#!/usr/bin/python3
# Start by importing the requisite modules and classes 

# matrix_synapse_automator_scripts/invite_acceptor_script.py

"""Lists, Accepts or rejects the invites recieved for a user."""
import asyncio
from nio import AsyncClient, InviteMemberEvent
from automation_helper import Callbacks
from time import sleep

# Script completes following tasks: 
# accept the invites automatically
# write the room_ids and their displayNames 

from dotenv import load_dotenv
import os

import logging

# preparing the logging config
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d-%b',
                    level=logging.INFO)

async def main() -> None:
    load_dotenv()
    user = input("Provide the server user id: [@user:dom.sample.in] ")
    password = input("Provide the password: ") 
    if user != "":
        client = AsyncClient(os.environ.get("SERVER"),user)
        logging.info(await client.login(password))
    else: 
        client = AsyncClient(os.environ.get("SERVER"),os.environ.get("MATUSER"))
        logging.info(await client.login(os.environ.get("PASS")))

    callback = Callbacks(client)
    decide = input("Enter 1 if you want to accept Invites, 2 to reject invites or just press enter to list the invites: ")
    if decide == "1":
        logging.info("Starting to accept invites\n")
        client.add_event_callback(callback.invite_callback, (InviteMemberEvent,))
        since_token = input("Provide a next_batch token if you have: ")

        if since_token:
            sync_data = await client.sync(full_state=True, since=since_token)
        else:
            sync_data = await client.sync(full_state=True)

        logging.info(f"next_batch_token: {sync_data.next_batch}")
        await client.close()

    elif decide == "2":
        logging.info("Starting to reject invites\n")
        client.add_event_callback(callback.invite_rejector, (InviteMemberEvent))
        sync_data = await client.sync(full_state=True)
        logging.info(f"next_batch_token: {sync_data.next_batch}")
        await client.close()

    else:
        logging.info("Just displaying invites\n")
        client.add_event_callback(callback.invite_display, (InviteMemberEvent))
        sync_data = await client.sync(full_state=True)
        logging.info(f"next_batch_token: {sync_data.next_batch}")
        await client.close()

asyncio.run(main())
