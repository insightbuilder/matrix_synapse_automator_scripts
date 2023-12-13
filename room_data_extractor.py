#!/usr/bin/python3
# matrix_synapse_automator_scripts/room_data_extractor.py

"""Gets the room_id and extracts the data for the single room from the sqlite database"""
import sqlite3
from dotenv import load_dotenv
import os

import logging

# preparing the logging config
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%d-%b',
                    level=logging.INFO)

# connect with the database
conn = sqlite3.connect("matrix_rooms_data.db")

# create a cursor object
c = conn.cursor()

# provide the tablename
table_name = input("Provide the table name like [message_table_2023-12-11]: ")

# get room_id
room_id = input("provide the room id like [!mdHNjbGCMALYDY:example.domain.in]: ")
# execute a SQL query
c.execute(f"""SELECT * FROM {table_name} WHERE room_id = {room_id}""")

# fetch the data
result = c.fetchall()

c.close()

for row in result:
    logging.info(row)
