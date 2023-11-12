#!/usr/bin/python3
# Start by importing the requisite modules and classes 
import asyncio
from nio import AsyncClient, RoomMessageText
from automation_helper import message_callback
# Script that keeps syncing, and joining all the invites
from dotenv import load_dotenv
import os


async def main() -> None:
    load_dotenv()
    client = AsyncClient(os.environ.get("SERVER"),os.environ.get("USER"))
    print(await client.login(os.environ.get("PASS")))
    client.add_event_callback(message_callback, RoomMessageText)

    since_token = input("Provide since token if you have: ")
    if since_token:
        await client.sync_forever(timeout=30000, full_state=True, since=since_token)  # milliseconds
    else:
        await client.sync_forever(timeout=30000)  # milliseconds
asyncio.run(main())
