#! /usr/bin/env python3 

# taken from:
#    https://docs.python.org/3.4/howto/webservers.html
#    https://pythonspot.com/mysql-with-python/

import cgi

# enable debugging.  Note that the Python docs recommend this for testing, but
# say that it's a very bad idea to leave enabled in production, as it can leak
# information about your internal implementation.
import cgitb
cgitb.enable()

import MySQLdb

import private_no_share_dangerous_passwords as pnsdp



db = MySQLdb.connect(host   = pnsdp.SQL_HOST,
                     user   = pnsdp.SQL_USER,
                     passwd = pnsdp.SQL_PASSWD,
                     db     = pnsdp.SQL_DB)

cur = db.cursor()

print("----------- Games -----------")
cur.execute("SELECT * FROM games;")
for row in cur.fetchall():
    print(row)
print()

print("----------- Moves -----------")
cur.execute("SELECT * FROM moves;")
for row in cur.fetchall():
    print(row)
print()

