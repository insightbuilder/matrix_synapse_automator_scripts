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

The scripts are written with ease of reading, and ease of modifying in mind. These scripts are not tested for all scenarios. To reduce complexity involved user_interactivity, using the
yaml configuration files, wrappers that abstract the complexity has been avoided. This repo doesn't share any opinion on the style of the code, its just written for improving efficiency
of homeserver automation.

These scripts SHOULD NOT be used on production server, if you Don't Know. Output of executing the scripts will be your sole responsibility.

Happy Automating..
