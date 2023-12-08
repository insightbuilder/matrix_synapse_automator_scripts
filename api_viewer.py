#!/usr/bin/python3
# matrix_synapse_automator_scripts/api_viewer.py

"""Explores the objects created by the Matrix Nio framework by interacting
with your homeserver. 

This modules acts as a playground before you start coding your logic or 
solve a automation challenge in your home server.
"""
import asyncio
from nio import AsyncClient, SyncResponse, ClientConfig, RoomMessageText
from automation_helper import message_callback
from dotenv import load_dotenv
import os

import logging

# preparing the logging config
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d-%b',
                    level=logging.INFO)


async def main():
    load_dotenv()
    server = os.environ.get('SERVER') # "https://max.sample.in"
    user = os.environ.get("MATUSER") # "@demo:max.sample.in"
    password = os.environ.gett("PASS") # pass 

    config = ClientConfig(store_sync_tokens=True)

    # Complete the login process
    client = AsyncClient(server, user, store_path="/home/user", config = config)
    # client = AsyncClient(server, user)
    # login_var = await client.login(password)
    login_var = await client.login(password)

    # register the callback for the message event for getting the message logged to console
    client.add_event_callback(message_callback, RoomMessageText)

    # logging.info(dir(login_var)) # 'access_token', 'device_id', 'elapsed', 'end_time', 'from_dict', 'start_time', 'timeout', 'transport_response', 'user_id']
    # logging.info("access token", login_var.access_token)
    # logging.info("device_id", login_var.device_id)
    # logging.info("client start time", login_var.start_time)
    # logging.info("client end time", login_var.end_time)
    # logging.info("client user_id", login_var.user_id)
    # logging.info("client tport response", login_var.transport_response)

    # Do the first sync, which will pull everything and provide the next_batch 
    # Then comment it out
    # data_sync: SyncResponse = await client.sync()

    # logging.info(type(data))
    # logging.info(dir(data)) []
    # logging.info(data.account_data_events) # ['account_data_events', 'device_key_count', 
                                       # 'device_list', 'elapsed', 'end_time', 
                                       # 'from_dict', 'next_batch', 'presence_events', 
                                       # 'rooms', 'start_time', 'timeout', 'to_device_events', 
                                       # 'transport_response', 'uuid']
    # logging.info(data.device_list)
    # logging.info("data next batch: ", data_sync.next_batch)
    # logging.info("data Start Time: ", data_sync.start_time)
    # logging.info("data End Time: ", data_sync.end_time)
    # logging.info(data.rooms)
    # roomObjects = data_sync.rooms
    # logging.info(dir(roomObjects)) # [ 'invite', 'join', 'leave']

    next_data_sync: SyncResponse = await client.sync(since='s66207_9872_12_716_1548_1_160_1377_0_2', full_state=True)
    logging.info(next_data_sync.next_batch)
    # logging.info(next_data_sync) # return  Sync response until batch: s66185_9680_0_706_1509_1_160_1296_0_2
    # logging.info(dir(next_data_sync)) # Its SyncResponse object
    # logging.info('next data account sync events: ', next_data_sync.account_data_events)

    # logging.info("reaching to sync_forever and waiting...")
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
        logging.info(e)
        await client.close()
    # Worked with ease
    # commenting client.close() since sync_forever()
    # await client.close()

asyncio.run(main())