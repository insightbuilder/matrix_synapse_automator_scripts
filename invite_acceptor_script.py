#!/usr/bin/python3
# Start by importing the requisite modules and classes 

import asyncio
from nio import AsyncClient, InviteMemberEvent
from automation_helper import Callbacks
from time import sleep

# Script completes following tasks: 
# accept the invites automatically
# write the room_ids and their displayNames 

from dotenv import load_dotenv
import os


async def main() -> None:
    load_dotenv()
    client = AsyncClient(os.environ.get("SERVER"),os.environ.get("USER"))
    print(await client.login(os.environ.get("PASS")))
    callback = Callbacks(client)
    client.add_event_callback(callback.invite_callback, (InviteMemberEvent,))
    since_token = input("Provide a next_batch token if you have: ")

    if since_token:
        sync_data = await client.sync(full_state=True, since=since_token)
    else:
        sync_data = await client.sync(full_state=True)

    print("next_batch_token: ", sync_data.next_batch)
    await client.close()

asyncio.run(main())
