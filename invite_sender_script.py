# Start by importing the requisite modules and classes 

import asyncio
from nio import AsyncClient, RoomMessageText, InviteMemberEvent
from automation_helper import action_room_dm_create
from time import sleep
from uuid import uuid4

# Script completes following tasks: 
# accept the invites automatically
# write the room_ids and their displayNames 


async def main() -> None:
    print(f"The script is created to send invites from different users to a single end user for testing purposes only.")
    user = input("Provide your user_id: [userid] ")
    user_id = f"@{user}:max.reconline.in"

    client = AsyncClient("https://max.sample.in", user_id)
    print(await client.login("pass"))

    rand_id = str(uuid4()).split('-')[2]
    name = f"{user}_room_{rand_id}"
    roomAlias = f"{user}_{rand_id}_room"
    topic = f"room for testing {user_id} messages"

    target_user = "@demo8:max.sample.in"

    await action_room_dm_create(client, target_user, roomAlias, name, topic)
    await client.close()

asyncio.run(main())
