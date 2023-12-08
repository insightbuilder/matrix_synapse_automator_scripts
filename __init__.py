# matrix_synapse_automator_scripts/__init__.py

"""Automate the repetitive tasks on your Matrix Server.

Modules exported by this package:
- `automation_helper.py`: Provides several functions that is used by the executable scripts accompanying this package

Scripts present in this module:
- `.env`: This files has to be created by the user. This file can contain the username, password and other secret keys. 
- `api_viewer.py`: Used for exploring the objects created by the Matrix-nio, as it interacts with your matrix homeserver.
- `automation_helper.py`: 
- `gbot_msgsender_script.py`: Script that automates sending messages to the rooms that belongs to the any kind of Bots, like whatsappbot, gmessagesbot etc.
- `invite_acceptor_script.py`: Lists, accepts are rejects the invites that is pending for any user, with which the script is started with.
- `invite_sender_script.py`: Sends invite to any user in the matrix server.
- `listen_and_ai_reply.py`: Integrates with the Open AI's gpt3.5-turbo LLM, and provides replies to user messages directly in the Matrix Client.
- `message_sender.py`: Sends message to a given user inside the matrix server.
- `messages_sync_script.py`: Syncs messages from all the rooms of a single user. 
- `room_leave_forget.py`: Leaves and forgets a given room.
"""