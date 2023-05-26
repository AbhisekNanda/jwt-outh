import sqlite3
import json
import uuid
from passlib.context import CryptContext
import bcrypt

# Create a SQL connection to our SQLite database
con = sqlite3.connect("sql_app.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row

cur = con.cursor()

def check_email(signup_email):
    emails=[]
    q1="SELECT Email FROM users;"
    for email in cur.execute(q1):
        emails.append(email[0])
    if signup_email in emails:
        return True
    else :
        return False

#bugs need to be fixed
def create_userid():
    for i in cur.execute("SELECT MAX(id) from users"):
        pass
    return i[0]+1

def login(email,password):
    if check_email(email):
        q="select hashed_password from users where email=?"
        data=cur.execute(q,(email,)).fetchall()
        
        check_password=password.encode()
        result = bcrypt.checkpw(check_password, data[0][0])
        if result:
            q="select id,firstname,lastname,school from users where email=?"
            data=cur.execute(q,(email,)).fetchall()
            
            return {"id":data[0][0]}
        else :
            return {"status":"incorrect password"}
    else:
        return {"status":"invalid email"}