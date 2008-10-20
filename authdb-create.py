import sqlite3
import sys
conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()
c.execute('create table users (username text, password text)')
conn.commit()
c.close()
