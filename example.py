import os
from tswrapper import TRTLServices
import sqlite3
import json

#set token
os.environ["TRTL_SERVICES_TOKEN"] = "<TOKEN>"

#create sql db if not exist
conn = sqlite3.connect("./db.sqlite")

#open db connection
c = conn.cursor()

#create table if not exist
c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            id integer PRIMARY KEY AUTOINCREMENT,
            address text NOT NULL,
            balance decimal(24, 2) DEFAULT 0.00,
            locked decimal(24, 2) DEFAULT 0.00,
            blockIndex integer NOT NULL,
            scanIndex integer NOT NULL,
            created integer DEFAULT CURRENT_TIMESTAMP
        );""")

#create new address
new_address = json.loads(TRTLServices.createAddress())

#prepare db insert
address = new_address['address']
blockIndex = new_address['blockIndex']
payload = (address, blockIndex, blockIndex)

#store addresses
c.execute('INSERT INTO addresses (address, blockIndex, scanIndex) VALUES (?,  ? , ?)', payload)
conn.commit()

print('saved file to sql')

#grab addresses
for addresses in c.execute('SELECT * from addresses;'):
    print(addresses)

conn.commit()

#close connection
conn.close()
