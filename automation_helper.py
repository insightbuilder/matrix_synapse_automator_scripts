# matrix_synapse_automator_scripts/automation_helper.py

"""Provides several functions, classes with callback methods to
interact with your homeserver using python."""

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
import json
import logging
import sqlite3
# preparing the logging config
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d-%b',
                    level=logging.INFO)

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    """Callback that processes the messages recieved inside all the Matrix room 
 
    Args:
        room: Matrix room from which the message event has to be processed.
        event: List of room_ids as strings.
 
    Returns:
        Appends the room_id, event_id, room display_name, event timestamp, and
        event body to the json file, that is named with the date of processing."""


    logging.info(
        f"Message received in room {room.display_name}\n"
        # unix ts is converted to datetime instance, and the formatted to string format, that is required by us
        # divide the ts with 1000 to make it as seconds
        f"{room.user_name(event.sender)} | {event.body} | {datetime.fromtimestamp(event.server_timestamp / 1000)}"
    )
    date = datetime.now().strftime("%Y-%m-%d") # date objec
    file_name = f"message_collector_{date}.txt"

    # Reading and writing the messages to the file
    with open(file_name, 'a+') as msg_fobj:
        # loading the data from the file
        existing_data = {"room_id": room.room_id,
                 "event_id": event.event_id,
                 "display_name": room.display_name,
                 "timeStamp": str(datetime.fromtimestamp(event.server_timestamp / 1000)),
                 "user_name": room.user_name(event.sender),
                 "body": event.body}
        # Writing the new data into the file, by over-writing the existing data
        msg_fobj.write(str(existing_data) + ',')

async def message_callback_sqlite(room: MatrixRoom, event: RoomMessageText) -> None:
    """Callback that processes the messages recieved inside a specific Matrix room
    and writes the data to sqlite database table, whose name includes the date of 
    data extraction 

    Args:
        room: Matrix room from which the message event has to be processed.
        event: List of room_ids as strings.

    Returns:
        Writes the room_id, event_id, room display_name, event timestamp, and
        event body to the table inside sqlite database."""

    logging.info(
        f"Message received in room {room.display_name}\n"
        # unix ts is converted to datetime instance, and the formatted to string format, that is required by us
        # divide the ts with 1000 to make it as seconds
        f"{room.user_name(event.sender)} | {event.body} | {datetime.fromtimestamp(event.server_timestamp / 1000)}"
    )
    date = datetime.now().strftime("%Y_%m_%d") # date objec
    table_name = f"message_table_{date}"
    # creating database and connecting it
    conn = sqlite3.connect("matrix_rooms_data.db") 
    # create connection to the database
    cursor = conn.cursor()
    # create the table with above name, proceed further if it is not already created
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   room_id TEXT NOT NULL,
                   event_id TEXT NOT NULL,
                   room_display_name TEXT NOT NULL,
                   date_time TEXT NOT NULL,
                   room_user TEXT NOT NULL,
                   message_body TEXT NOT NULL
    )""")
    # Write the data to the table
    cursor.execute(f"""INSERT INTO {table_name} (room_id, event_id, room_display_name,
                    date_time, room_user, message_body) VALUES(?, ?, ?, ?, ?, ?)""",
                    (room.room_id.replace("!",""), event.event_id, room.display_name, 
                    str(datetime.fromtimestamp(event.server_timestamp / 1000)), 
                    room.user_name(event.sender), 
                    event.body))
    logging.info(f"Completed writing to {room.room_id} data to table")
    # commit the data to database through connection
    conn.commit()
    # close the connection
    conn.close()

class Callbacks(object):
    """Class initiated with the homeserver client which 
    gives access to the callback methods, that uses the client 
    to process the messages, invites."""
    def __init__(self, client):
        """Store the AsyncClient"""
        self.client = client

    async def ai_message_callback(self, room: MatrixRoom, event: RoomMessageText):
        """Returns the AI generated reply for the messages recieved in the
        given room, with the send_text_message function
        
        Args:
            room: Matrix Room in which the AI model is linked
            event: Room event that contains the data sent by the server
            
        Returns:
            None"""
        recieved_message = event.body
        room_id = room.room_id
 
        promptTemplate = """You are helpful and pleasant assistant, who can process any message 
        by thinking step by step. You are tasked to process the {message}.
        Follows the instructions provided in the message and provide the reply."""

        if event.sender != self.client.user_id:
            prompt = PromptTemplate.from_template(promptTemplate)
            load_dotenv()

            processor = prompt | ChatOpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY')) | StrOutputParser()
            output = processor.invoke({"message": recieved_message})

            logging.info(f"room_id: {room_id}, chatgpt: {output}")

            await send_text_message(self.client, room_id, output)

    async def invite_rejector(self, room: MatrixRoom, event: InviteMemberEvent):
        """Rejects the invite recieved for a logged in user for the given 
        room. 
        Args:
            room: Matrix Room in which the AI model is linked
            event: Invite member Room event sent by the server
    
        Returns:
            None"""
        logging.info("*******Invite Rejection Start*********")
        logging.info(f"Message callback from room {room.room_id} recieved this.")
        logging.info(f"Event Sender: {event.sender}")
        logging.info(f"Display Name: {event.content['displayname']}")
        if event.membership == "invite":
            logging.info("Rejecting the invite membership event")
            await self.client.room_leave(room.room_id)
            logging.info(f"rejected the room {room.room_id} successfully.")
     
    async def invite_display(self, room:MatrixRoom, event: InviteMemberEvent):
        """Rejects the invite recieved for a logged in user for the given 
        room. 

        Args:
            room: matrix room in which the ai model is linked
            event: invite member room event sent by the server
 
        Returns:
            none"""

        logging.info(f"Message callback from room {room.room_id} recieved this.")
        logging.info(f"Event Sender: {event.sender}")
        logging.info(f"Display Name: {event.content['displayname']}")


    async def invite_callback(self, room: MatrixRoom, event: InviteMemberEvent):
        """Rejects the invite recieved for a logged in user for the given 
        room.

        Args:
            room: matrix room in which the ai model is linked
            event: invite member room event sent by the server

        Returns:
            None"""

        logging.info("*******Invite Callback detail Start*********")
        logging.info(f"Message callback from room {room.room_id} recieved this.")
        logging.info(f"Event: {event}.")
        logging.info(f"Event Sender: {event.sender}")
        logging.info(f"Event shows membership: {event.membership}")
        logging.info("*******Invite Callback detail End*********")
        if event.membership == "join":
            logging.info(f"Display Name: {event.content['displayname']}")
        date = datetime.now().strftime("%Y-%m-%d") # date objec
        file_name = f"room_id_displayname_{date}.csv"

        if event.membership == "invite":
            logging.info("Processing the invite membership event")
            result = await self.client.join(room.room_id)
            if type(result) is JoinError:
                logging.info("Error in Joining the Room")

            else:
                logging.info(f"Joined the room {room.room_id} successfully.")
                with open(file_name, '+a') as file_obj:
                    file_obj.write(f"{room.room_id, event.content['displayname'], event.sender.split(':')[0].replace('@','')}\n")


async def action_room_dm_create(client: AsyncClient, tgt_user, roomAlias, name, topic):
    """Create a direct message (DM) room while already being logged in.
    After creating the private DM room it invites the other user to it.
    Purpose of the script is to send invites from the command line,
    where the client is already logged in using the user_name, who is sending the dm.
    Name of the room is created using random numbers, so the existing
    room conflicts are avoided.
    Args:
        client: AsyncClient: nio client, allows as to query the server
        credentials: dict: allows to get the user_id of sender, etc
        user : User to create DM rooms with
    Returns:
        None
    """
    # room_aliases: Created with {user_name}_{uuid}_{date}
    # topic : {user_name}_topic_discussion_{uuid}

    logging.info(
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
        logging.info(
             "E125: "
             "Room_create failed with response: "
             f"{str(resp)}"
         )
    else:
        logging.info(f"Invite to {tgt_user} succeeded")


async def send_text_message(client: AsyncClient, room_id: str, message: str):

    message = message.strip('\n')

    if message.strip() == "":
        logging.info("message is empty. Dropping it")

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
            logging.info("Sending message failed")
    except Exception as e:
        logging.info(e)
        logging.info("Sending message failed. Sorry about that")


def is_ten_digits(string):
    """Checks if a string contains ten numbers only.
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


async def action_joined_members(client: AsyncClient, room: str) -> List[RoomMember]:
    """Return the members joined in a given room
   
    Args:
        client: Roomserver client logged in using username and password
        room: Room_id in string format
       
    Returns:
        String of member names invited into the room"""

    room = room.replace(r"\!", "!")
    resp = await client.joined_members(room)
    if isinstance(resp, JoinedMembersError):
        logging.info(f"Joined members failed with {resp}")

    text = resp.room_id
    for member in resp.members:
        text += (";" + member.user_id + ";"
                + member.display_name + "\n")
        text = text.strip()
        return text


async def action_joined_rooms(client: AsyncClient) -> List[MatrixRoom]:
    """Return the list of rooms joined by the user logged into the Client
  
    Args:
        client: Roomserver client logged in using username and password
      
    Returns:
        List of room_id in which the user is part of."""

    resp = await client.joined_rooms()
 
    if isinstance(resp, JoinedRoomsError):
        logging.info(f"Joined rooms failed with {str(resp)}")
    else:
        logging.info(f"Joined rooms success with {str(resp)}")

    return resp.rooms

room_members = Dict[str, List[RoomMember]]

async def return_room_members(client: AsyncClient, rooms_list: List[str]) -> List[room_members]:
    """Extracts the members of multiple rooms 
  
    Args:
        client: Roomserver client logged in using username and password.
        rooms_list: List of room_ids as strings.
    
    Returns:
        List of dictionaries of room and its joined members"""

    room_members = []

    for room in rooms_list:

        joined_members = await action_joined_members(client, room)

        room_members.append({room: joined_members})

    return room_members
