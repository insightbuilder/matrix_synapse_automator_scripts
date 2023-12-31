#!/usr/bin/python3

# matrix_synapse_automator_scripts/gbot_msgsender_script.py

"""Script that sends message to the Bots, for automating room invites."""

import asyncio
from nio import AsyncClient 
from automation_helper import is_ten_digits, send_text_message
from time import sleep
import os
from dotenv import load_dotenv

# Script completes following tasks: 
# Send the dm messages to google messages bot   

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

    file_path = input("Provide the path of the file that contains Phone numbers list: ")

    try:
        # If the file name is wrong exit cleanly
        with open(file_path, 'r') as phone:
            number_list = phone.readlines()

        # Get the room_id of the gmessages bot, after completing the login process
        gmsg_bot_room = input("Enter the gmessages bot room_id: '!xxxxxxx:sam.pleserver.com' ") 

        sync_data = await client.sync(full_state=True)
        logging.info(f"Note down the next_batch token: {sync_data.next_batch}")

        for num in number_list:
            num = is_ten_digits(num)
            if num:
                message = f"pm {num}"
                # Send the message 
                await send_text_message(client, gmsg_bot_room, message)
                # After each dm, sleep for 10 sec, so the server can process
                sleep(10)
            else:
                logging.info(f"{num} seems to be invalid phonenumber, skipping it. Kindly re-check and input again.")

        await client.close()

    except Exception as e:
            logging.info(e) 
            await client.close()

asyncio.run(main())