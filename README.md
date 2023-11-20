# matrix_synapse_automator_scripts

PS : READ AND UNDERSTAND THE SCRIPTS **BEFORE EXECUTING** ON YOUR SERVER's Terminal

Repo contains Python scripts that enable automation, information gathering and help in learning more about the Synapse and the Matrix Server APIs
The scripts are written after reviewing many bots that were written on [Matrix Nio Framework](https://matrix-nio.readthedocs.io/)

## Objective

Write python scripts for Automating Synapse server opertation, which are simple and accessible for
    1) a user / programmer who is new to Python / Synapse Server  

    2) hobbyists / end users who want simple re-usable scripts to automate their tasks
    
    3) server administrators / moderators who are learning to code their own bots 

    4) tinkerers who want to slightly under the hood of Matrix Server 

### Scripts break-up

- automation_helper.py : Contains the Async functions and Callbacks that do the heavy lifting

- messages_sync_script.py : Takes care of downloading only the text messages from the server. Contains a callback which process the messages recieved in server

- message_sender.py : Script that reads the file containing the room_ids, and sends a single message to all the rooms in that file

- invite_acceptor_script.py : Contains the callback that accepts the invites recieved by a logged-in user, and writes the Room_id, Invitee, and Inviter details

- invite_sender_script.py : Script that creates dm_rooms inside the server, between a Target_user who is hard-coded in the script, and multiple other users

- gbot_msgsender_script : Script that accepts the GmessagesBot Room_Id and sends messages to that room. These messages can be used for commands to gmessagesbot

- room_leave_forget.py : Script to leave a set of rooms or all the rooms for a particular user

The scripts are written with ease of reading, and ease of modifying in mind. These scripts are not tested for all scenarios. To reduce complexity involved user_interactivity, using the
yaml configuration files, wrappers that abstract the complexity has been avoided. This repo doesn't share any opinion on the style of the code, its just written for improving efficiency
of homeserver automation.

These scripts SHOULD NOT be used on production server, if you Don't Know. Output of executing the scripts will be your sole responsibility.

Happy Automating..

### Version Updates

* v0.2 : 12-Nov-2023 : InsightBuilder

    - Worked on the api_viewer.py script to explore the sync() and the sync_forever() methods 

    - Importing python-dotenv module so the user, password and server variables can be accessed from the .env file. 
    Place the .env file in the root of the folder. .env file example as follows.
    
    ''' 
    .env file:
    OPENAI_API_KEY="yourKey"
    SERVER="ur.homeserver.in"
    USER="@demo:ur.homeserver.in"
    PASS="1thetd"
    '''
    
    - Added sync_data variable in scripts to get the next_batch token before executing any operation. 
    The next_batch token can be used when trying to sync messages or invites from a particular token
    This will save bandwidth, and token charges (if using AI models)

    - Updated gbot_msgsender_script with try except block to catch if the file provided is not present

    - Incorporated user password input option in the scripts, if environment variable creates issue

    - Create room_leave_forget script to bulk leave the rooms for a given user

    - Updated the automation_helper.py to include callbacks for invite_rejector and invite_display
    
    - Created option in invite_acceptor_script to accept, list or reject the invites under a user name

    - Started printing out the next_batch token in the scripts before performing any action, or callback. 
    Can use this token as "Since_token" and sync the server from that token time onwards

* v0.21: 20-Nov-2023 : InsightBuilder

     - Incorporated logging in place of the print statements in all the scripts. The log will have the following 
     format
        20-Nov | INFO | message to be shared
    
    - Updated the Message Sender script to read the messages from a file, and then send it to the rooms.