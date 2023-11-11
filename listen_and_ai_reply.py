# Start by importing the requisite modules and classes 
import asyncio
from nio import AsyncClient, RoomMessageText
from automation_helper import ai_message_callback
# Script that keeps syncing, and joining all the invites


async def main() -> None:
    client = AsyncClient("https://max.sample.in", "@demo8:max.sample.in")
    print(await client.login("pass"))
    client.add_event_callback(ai_message_callback, RoomMessageText)
    await client.sync_forever(timeout=30000)  # milliseconds

asyncio.run(main())
