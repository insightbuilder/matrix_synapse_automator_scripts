# The helper script for the automator

from typing import List, Dict
import asyncio
from time import sleep
from datetime import datetime
from nio import (AsyncClient, MatrixRoom, RoomMessageText, InviteMemberEvent,
                 RoomAliasEvent, RoomMemberEvent, SyncError, SyncResponse,
                 JoinedRoomsError, RoomMember, JoinedMembersError, JoinError,
                 RoomSendError, RoomVisibility, RoomCreateError, RoomPreset)
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from dotenv import load_dotenv
import os


async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    """
    Message recieved by the user inside the server using the 
    sync method.
    Output : room_name,user_name, message_text
    """
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )
    date = datetime.now().strftime("%Y-%m-%d") # date objec
    file_name = f"message_collector_{date}.txt"
    # Writing the messages to the file

    with open(file_name, 'a+') as msg_fobj:
        msg_fobj.write(f"{room.display_name},{room.user_name(event.sender)}, {event.body}\n")


class Callbacks(object):
    """Class to pass client to callback method"""
    def __init__(self, client):
        """Store the AsyncClient"""
        self.client = client

    async def ai_message_callback(self, room: MatrixRoom, event: RoomMessageText):
        # recieved_message = callback recieves the message via event.body
        # room_id = extracted from room.room_id
        recieved_message = event.body
        room_id = room.room_id
        promptTemplate = """You are helpful and pleasant assistant, who can process any message 
        by thinking step by step. You are tasked to process the {message}.
        Follows the instructions provided in the message and provide the reply."""
        prompt = PromptTemplate.from_template(promptTemplate)
        load_dotenv()
        processor = prompt | ChatOpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY')) | StrOutputParser()
        output = processor.invoke({"message": recieved_message})
        print(f"room_id: {room_id}, chatgpt: {output}")
        await send_text_message(self.client, room_id, output)

    async def invite_callback(self, room: MatrixRoom, event: InviteMemberEvent):
        print("*******Invite Callback detail Start*********")
        print(f"Message callback from room {room.room_id} recieved this.")
        print(f"Event: {event}.")
        print("Event Sender: ", event.sender)
        print("Event shows membership", event.membership)
        print("*******Invite Callback detail End*********")
        if event.membership == "join":
            print("Display Name: ", event.content['displayname'])
        date = datetime.now().strftime("%Y-%m-%d") # date objec
        file_name = f"room_id_displayname_{date}.csv"

        if event.membership == "invite":
            print("Processing the invite membership event")
            result = await self.client.join(room.room_id)
            if type(result) is JoinError:
                print("Error in Joining the Room")

            else:
                print(f"Joined the room {room.room_id} successfully.")
                with open(file_name, '+a') as file_obj:
                    file_obj.write(f"{room.room_id, event.content['displayname'], event.sender.split(':')[0].replace('@','')}\n")


async def action_room_dm_create(client: AsyncClient, tgt_user, roomAlias, name, topic):
    """Create a direct message (DM) room while already being logged in.
    After creating the private DM room it invites the other user to it.
    Purpose of the script is to send invites from the command line,
    where the client is already logged in using the user_name, who is sending the dm.
    Name of the room is created using random numbers, so the existing
    room conflicts are avoided.
    Arguments:
    ---------
    client: AsyncClient: nio client, allows as to query the server
    credentials: dict: allows to get the user_id of sender, etc
    user : User to create DM rooms with
    """
    # room_aliases: Created with {user_name}_{uuid}_{date}
    # topic : {user_name}_topic_discussion_{uuid}

    print(
         f'Creating DM room with user "{tgt_user}", '
         f'room alias "{roomAlias}", '
         f'name "{name}", topic "{topic}" and '
     )

    # nio's room_create does NOT accept "#foo:example.com"
    resp = await client.room_create(
         alias=roomAlias,  # desired canonical alias local part, e.g. foo
         visibility=RoomVisibility.private,
         is_direct=True,
         preset=RoomPreset.private_chat,
         invite={tgt_user},  # invite the user to the DM
         name=name,  # room name
         topic=topic,  # room topic
         initial_state=())
    if isinstance(resp, RoomCreateError):
        print(
             "E125: "
             "Room_create failed with response: "
             f"{str(resp)}"
         )
    else:
        print(f"Invite to {tgt_user} succeeded")
 

async def send_text_message(client, room_id, message):
    """Sends simple text message to a single room.
    Need this for sending multiple messages to gmessages room"""

    message = message.strip('\n')

    if message.strip() == "":
        print("message is empty. Dropping it")

    content = {"msgtype": "m.text"}

    content["body"] = message

    try:
        resp = await client.room_send(
            room_id,
            message_type="m.room.message",
            content=content,
            ignore_unverified_devices=True
        )
        if isinstance(resp, RoomSendError):
            print("Sending message failed")
    except Exception as e:
        print(e)
        print("Sending message failed. Sorry about that")


def is_ten_digits(string):
    """
    Checks if a string contains ten numbers only.
    Args:
      string: The string to check.
    Returns:
      True if the string contains ten numbers only, False otherwise.
    """

    string = string.strip()
    if " " in string:
        string.replace(" ", "")
    if len(string) != 10:
        return False

    if all(c.isdigit() for c in string):
        return string


async def action_joined_members(client: AsyncClient, room) -> List[RoomMember]:
    room = room.replace(r"\!", "!")
    resp = await client.joined_members(room)
    if isinstance(resp, JoinedMembersError):
        print(f"Joined members failed with {resp}")
 
    text = resp.room_id
    for member in resp.members:
        text += (";" + member.user_id + ";"
                + member.display_name + "\n")
        text = text.strip()
        return text


async def action_joined_rooms(client: AsyncClient):
    """The list of joined rooms will be returned"""

    resp = await client.joined_rooms()
    if isinstance(resp, JoinedRoomsError):
        print(f"Joined rooms failed with {str(resp)}")
    else:
        print(f"Joined rooms success with {str(resp)}")

    return resp.rooms


async def return_room_members(client: AsyncClient, rooms_list) -> List[Dict]:
    """Returns dictionary of room_id:[room_members]"""
    room_members = []

    for room in rooms_list:

        joined_members = await action_joined_members(client, room)

        room_members.append({room: joined_members})

    return room_members


