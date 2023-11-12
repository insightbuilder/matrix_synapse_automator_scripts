#!/usr/bin/python3
# Start by importing the requisite modules and classes 
import asyncio
from nio import AsyncClient, RoomMessageText
from automation_helper import Callbacks
# Script that keeps syncing, and joining all the invites


from dotenv import load_dotenv
import os


async def main() -> None:
    load_dotenv()
    user = input("Provide the server user id: [@user:dom.sample.in] ")
    password = input("Provide the password: ") 
    if user != "":
        client = AsyncClient(os.environ.get("SERVER"),user)
        print(await client.login(password))
    else: 
        client = AsyncClient(os.environ.get("SERVER"),os.environ.get("USER"))
        print(await client.login(os.environ.get("PASS")))

    since_token = input("Provide since token if you have: ") 

    callback = Callbacks(client)
    client.add_event_callback(callback.ai_message_callback, RoomMessageText)
    if since_token:
        print(f"Syncing messages using the {since_token}")
        await client.sync_forever(timeout=30000, full_state=True, since=since_token)  # milliseconds
    else:
        print("Syncing all the messages")
        await client.sync_forever(timeout=30000)  # milliseconds
asyncio.run(main())
