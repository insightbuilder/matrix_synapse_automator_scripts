# Start by importing the requisite modules and classes 

import asyncio
from nio import AsyncClient, InviteMemberEvent
from automation_helper import Callbacks
from time import sleep

# Script completes following tasks: 
# accept the invites automatically
# write the room_ids and their displayNames 


async def main() -> None:
    client = AsyncClient("https://max.sample.in", "@demo8:max.sample.in")
    # client = AsyncClient(server, user_id)
    print(await client.login("pass"))

    callback = Callbacks(client)

    client.add_event_callback(callback.invite_callback, (InviteMemberEvent,))
    await client.sync_forever(timeout=30000)

asyncio.run(main())
