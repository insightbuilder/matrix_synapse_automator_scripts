#!/usr/bin/python3
# matrix_synapse_automator_scripts/updated_message_collector.py

"""Collects and writes the message from all the room and writes to sqlite database."""
import asyncio
from nio import AsyncClient, InviteMemberEvent, RoomMessageText
from automation_helper import message_callback_sqlite
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
        client = AsyncClient(os.environ.get("SERVER"), user)
        logging.info(await client.login(password))
    else: 
        client = AsyncClient(os.environ.get("SERVER"), os.environ.get("MATUSER"))
        logging.info(os.environ.get("PASS"))
        logging.info(await client.login(os.environ.get("PASS")))

        client.add_event_callback(message_callback_sqlite, RoomMessageText)

        since_token = input("Provide a next_batch token if you have: ")
        try:
            if since_token:
                sync_data = await client.sync(full_state=True, since=since_token)
            else:
                sync_data = await client.sync(full_state=True)

            logging.info(f"next_batch_token: {sync_data.next_batch}")
            await client.logout()
        except Exception as e:
            logging.info(f"Errored out by {e}")
            await client.close()

asyncio.run(main())
