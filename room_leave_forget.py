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

     
    sync_data = await client.sync(full_state=True)
    print("Make note of the next_batch token: ", sync_data.next_batch)

    # Printing the list of joined rooms 
    joinedRooms = await client.joined_rooms()
    room_list = joinedRooms.rooms
    print(room_list, end='\n')

    # Provide option to leave and forget a single, list of rooms or all the rooms
    leave_rooms = input("Enter room ids you want to leave seperated with a ',' or just press enter to leave all rooms :")
    if leave_rooms != "":
        if ',' in leave_rooms:
            leave_list = leave_rooms.split(',')
            for r_id in leave_list:
                print(await client.room_leave(room_id=r_id))
                print(await client.room_forget(room_id=r_id))

    else:
        for r_id in room_list:
            print(await client.room_leave(room_id=r_id))
            print(await client.room_forget(room_id=r_id))

    print("Closing the connection to Client. Thanks...")

    await client.close()

asyncio.run(main())