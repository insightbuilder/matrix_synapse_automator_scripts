#!/usr/bin/python3
# Start by creating a basic client 
import asyncio
from time import sleep
from nio import (AsyncClient, RoomSendError)
from automation_helper import send_text_message
import logging

# preparing the logging config
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d-%b',
                    level=logging.INFO)

# Script takes the file containing room_ids and sends a single message 
# to all rooms
import os
from dotenv import load_dotenv

async def main() -> None:
    load_dotenv()
    user = input("Provide the server user id: [@user:dom.sample.in] ")
    password = input("Provide the password: ") 
    if user != "":
        client = AsyncClient(os.environ.get("SERVER"),user)
        logging.info(await client.login(password))
    else: 
        client = AsyncClient(os.environ.get("SERVER"),os.environ.get("USER"))
        logging.info(await client.login(os.environ.get("PASS")))

    sync_data = await client.sync(full_state=True)
    logging.info("Make note of the next_batch token: ", sync_data.next_batch)

    print("************************************************")
    print("Prepare a text file with the message you want to send. Keep it same folder as this script")
    print("*************************************************")
    message_file = input("Provide the file that contains the message: ")

    with open(message_file, mode="r"):
        message_send = message_file.read()

    logging.info(f"""Message to be sent is :
                 {message_send}
                 """)
    file_path = input("Provide the path of the file that contains Room_id list: ")

    with open(file_path, 'r') as phone:
        number_list = phone.readlines()

    # split the numbers into individual contacts 
    for data in number_list:
        # When reading from files, all the punctuations have to be removed. 
        data = data.replace("(", "").replace(")", "").replace("'", "").replace("'", "")
        data = data.strip()
        room_id = data.split(',')[0]
        logging.info(room_id)
        # Send the message 
        logging.info(f"Sending message to room belonging to {data.split(',')[1]}\n")
        await send_text_message(client, room_id, message_send)
        # After each dm, sleep for 10 sec, so the server can process
        sleep(2)
    # Close the client session
    await client.close()

asyncio.run(main())
