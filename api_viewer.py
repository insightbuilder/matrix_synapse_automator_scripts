#!/usr/bin/python3
import asyncio
from nio import AsyncClient, SyncResponse, ClientConfig, RoomMessageText
from automation_helper import message_callback
from dotenv import load_dotenv
import os

async def main():
    load_dotenv()
    server = os.environ.get('SERVER') # "https://max.sample.in"
    user = os.environ.get("USER") # "@demo:max.sample.in"
    password = os.environ.gett("PASS") # pass 

    config = ClientConfig(store_sync_tokens=True)

    # Complete the login process
    client = AsyncClient(server, user, store_path="/home/user", config = config)
    # client = AsyncClient(server, user)
    # login_var = await client.login(password)
    login_var = await client.login(password)

    # register the callback for the message event for getting the message printed to console
    client.add_event_callback(message_callback, RoomMessageText)

    # print(dir(login_var)) # 'access_token', 'device_id', 'elapsed', 'end_time', 'from_dict', 'start_time', 'timeout', 'transport_response', 'user_id']
    # print("access token", login_var.access_token)
    # print("device_id", login_var.device_id)
    # print("client start time", login_var.start_time)
    # print("client end time", login_var.end_time)
    # print("client user_id", login_var.user_id)
    # print("client tport response", login_var.transport_response)

    # Do the first sync, which will pull everything and provide the next_batch 
    # Then comment it out
    # data_sync: SyncResponse = await client.sync()

    # print(type(data))
    # print(dir(data)) []
    # print(data.account_data_events) # ['account_data_events', 'device_key_count', 
                                       # 'device_list', 'elapsed', 'end_time', 
                                       # 'from_dict', 'next_batch', 'presence_events', 
                                       # 'rooms', 'start_time', 'timeout', 'to_device_events', 
                                       # 'transport_response', 'uuid']
    # print(data.device_list)
    # print("data next batch: ", data_sync.next_batch)
    # print("data Start Time: ", data_sync.start_time)
    # print("data End Time: ", data_sync.end_time)
    # print(data.rooms)
    # roomObjects = data_sync.rooms
    # print(dir(roomObjects)) # [ 'invite', 'join', 'leave']

    next_data_sync: SyncResponse = await client.sync(since='s66207_9872_12_716_1548_1_160_1377_0_2', full_state=True)
    print(next_data_sync.next_batch)
    # print(next_data_sync) # return  Sync response until batch: s66185_9680_0_706_1509_1_160_1296_0_2
    # print(dir(next_data_sync)) # Its SyncResponse object
    # print('next data account sync events: ', next_data_sync.account_data_events)

    # print("reaching to sync_forever and waiting...")
    # data: SyncResponse = await client.sync_forever(30000, full_state=True, since=data_sync.next_batch)
    # There is no data in the console, when the message is sent to logged in user even when sync_forever

    # Not working...
    # await client.sync_forever(30000, full_state=True, since=data_sync.next_batch)

    # Not Working... because there was no message_callback attached. Then worked
    await client.close()
    try:
        # sync_forever pulls all the messages till a arbitrary point
        # await client.sync_forever(30000) 
        # sync_forever with below option only pulls the messages from a particular token
        # No point in creating the variable on the below function and getting the next_batch
        pass 
        # await client.sync_forever(30000, full_state=True, since="s66200_9802_34_715_1540_1_160_1351_0_2")
    except Exception as e:
        print(e)
        await client.close()
    # Worked with ease
    # commenting client.close() since sync_forever()
    # await client.close()

asyncio.run(main())

    