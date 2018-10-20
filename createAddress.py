import os
from tswrapper import TRTLServices
import sqlite3
import json

os.environ["TRTL_SERVICES_TOKEN"] = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoieW8iLCJhcHBJZCI6MjAsInVzZXJJZCI6MiwicGVybWlzc2lvbnMiOlsiYWRkcmVzczpuZXciLCJhZGRyZXNzOnZpZXciLCJhZGRyZXNzOmFsbCIsImFkZHJlc3M6c2NhbiIsImFkZHJlc3M6ZGVsZXRlIiwidHJhbnNmZXI6bmV3IiwidHJhbnNmZXI6dmlldyJdLCJpYXQiOjE1Mzk5OTQ4OTgsImV4cCI6MTU3MTU1MjQ5OCwiYXVkIjoiZ2FuZy5jb20iLCJpc3MiOiJUUlRMIFNlcnZpY2VzIiwianRpIjoiMjIifQ.KkKyg18aqZfLGMGTnUDhYQmVSUoocrr4CCdLBm2K7V87s2T-3hTtM2MChJB2UdbDLWnf58GiMa_t8xp9ZjZjIg"

conn = sqlite3.connect("./db.sqlite")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            id integer PRIMARY KEY AUTOINCREMENT,
            address text NOT NULL,
            balance decimal(24, 2) DEFAULT 0.00,
            locked decimal(24, 2) DEFAULT 0.00,
            blockIndex integer NOT NULL,
            scanIndex integer NOT NULL,
            created integer DEFAULT CURRENT_TIMESTAMP
        );""")

new_address = json.loads(TRTLServices.createAddress())

print(new_address)

address = new_address['address']
blockIndex = new_address['blockIndex']

payload = (address, blockIndex, blockIndex)

c.execute('INSERT INTO addresses (address, blockIndex, scanIndex) VALUES (?,  ? , ?)', payload)
conn.commit()
conn.close()

print('saved file to sql')