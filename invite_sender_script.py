#!/usr/bin/python3
# Start by importing the requisite modules and classes 

import asyncio
from nio import AsyncClient, RoomMessageText, InviteMemberEvent
from automation_helper import action_room_dm_create
from time import sleep
from uuid import uuid4

# Script completes following tasks: 
# accept the invites automatically
# write the room_ids and their displayNames 

from dotenv import load_dotenv
import os


async def main() -> None:
    print(f"The script is created to send invites from different users to a single end user for testing purposes only.")
    user = input("Provide your user_id: [userid] ")
    user_id = f"@{user}:max.reconline.in"
    load_dotenv()
    client = AsyncClient(os.environ.get("SERVER"),user_id)
    print(await client.login(os.environ.get("PASS")))

    rand_id = str(uuid4()).split('-')[2]
    name = f"{user}_room_{rand_id}"
    roomAlias = f"{user}_{rand_id}_room"
    topic = f"room for testing {user_id} messages"

    target_user = "@demo9:max.reconline.in"
    sync_data = await client.sync(full_state=True)
    print("make note of this next_batch token: ", sync_data.next_batch)

    await action_room_dm_create(client, target_user, roomAlias, name, topic)

    await client.close()

asyncio.run(main())
