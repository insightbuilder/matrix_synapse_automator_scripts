# Start by creating a basic client 
import asyncio
from time import sleep
from nio import (AsyncClient, RoomSendError)
from automation_helper import send_text_message

# Script takes the file containing room_ids and sends a single message 
# to all rooms
 

async def main() -> None:
    client = AsyncClient("https://max.sample.in", "@demo8:max.sample.in")
    print(await client.login("pass"))

    file_path = input("Provide the path of the file that contains Room_id list: ")
    message_send = input("Provide the message to be sent: ")

    with open(file_path, 'r') as phone:
        number_list = phone.readlines()

    # split the numbers into individual contacts 
    for data in number_list:
        # When reading from files, all the punctuations have to be removed. 
        data = data.replace("(", "").replace(")", "").replace("'", "").replace("'", "")
        data = data.strip()
        room_id = data.split(',')[0] 
        print(room_id)
        # Send the message 
        print(f"Sending message to room belonging to {data.split(',')[1]}\n")
        await send_text_message(client, room_id, message_send)
        # After each dm, sleep for 10 sec, so the server can process
        sleep(2)
    # Close the client session
    await client.close()

asyncio.run(main())