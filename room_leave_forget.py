#!/usr/bin/python3
# Start by creating a basic client 
import asyncio
from time import sleep
from nio import (AsyncClient, RoomSendError)
from automation_helper import send_text_message

# Script gets all the rooms the user is part of, and lists them first
# Gives option to leave and forget a single room, a list of rooms or all the rooms 

import os
from dotenv import load_dotenv

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
     
    sync_data = await client.sync(full_state=True)
    logging.info(f"Make note of the next_batch token: {sync_data.next_batch}")

    # logging the list of joined rooms 
    joinedRooms = await client.joined_rooms()
    room_list = joinedRooms.rooms
    # logging.info(room_list)
    decide = input("Choose 1 to exit script, 2 to start leave room script: ")
    if decide == "1":
        logging.info("leaving script. Rooms are intact...")
        await client.close()
    elif decide == "2":
        # Provide option to leave and forget a single, list of rooms or all the rooms
        leave_rooms = input("Enter room ids you want to leave seperated with a ',' or just press enter to leave all rooms :")
        if leave_rooms != "":
            if ',' in leave_rooms:
                leave_list = leave_rooms.split(',')
                for r_id in leave_list:
                    logging.info(await client.room_leave(room_id=r_id))
                    logging.info(await client.room_forget(room_id=r_id))

        else:
            for r_id in room_list:
                logging.info(await client.room_leave(room_id=r_id))
                logging.info(await client.room_forget(room_id=r_id))

        logging.info("Closing the connection to Client. Thanks...")

        await client.close()

asyncio.run(main())