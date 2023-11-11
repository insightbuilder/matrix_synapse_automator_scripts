# Start by importing the requisite modules and classes 

import asyncio
from nio import AsyncClient 
from automation_helper import is_ten_digits, send_text_message
from time import sleep

# Script completes following tasks: 
# Send the dm messages to google messages bot   


async def main() -> None:
    client = AsyncClient("https://max.sample.in", "@demo8:max.sample.in")

    # client = AsyncClient(server, user_id)
    print(await client.login("pass"))
    # "Logged in as @demo8:max.example.in device id: RANDOMDID"
    file_path = input("Provide the path of the file that contains Phone numbers list.")

    with open(file_path, 'r') as phone:
        number_list = phone.readlines()

    # Get the room_id of the gmessages bot, after completing the login process
    gmsg_bot_room = input("Enter the gmessages bot room_id: '!xxxxxxx:sam.pleserver.com' ") 

    for num in number_list:
        num = is_ten_digits(num)
        if num:
            message = f"pm {num}"
            # Send the message 
            await send_text_message(client, gmsg_bot_room, message)
            # After each dm, sleep for 10 sec, so the server can process
            sleep(10)
        else:
            print(f"{num} seems to be invalid phonenumber, skipping it. Kindly re-check and input again.")

    client.close()

asyncio.run(main())