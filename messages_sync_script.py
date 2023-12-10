#!/usr/bin/python3
# Start by importing the requisite modules and classes 

# matrix_synapse_automator_scripts/api_viewer.py

"""Syncs the events of a user from the server"""
import asyncio
from nio import AsyncClient, RoomMessageText
from automation_helper import message_callback
# Script that keeps syncing, and joining all the invites
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
        logging.info(await client.login(os.environ.get("PASS")))

    client.add_event_callback(message_callback, RoomMessageText)

    since_token = input("Provide since token if you have: ")
    if since_token:
        await client.sync_forever(timeout=30000, full_state=True, 
                                  since=since_token)  # milliseconds
    else:
        await client.sync_forever(timeout=30000)  # milliseconds
asyncio.run(main())
