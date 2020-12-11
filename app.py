import mariadb
from flask import Flask, request, Response
from flask_cors import CORS
import json
import dbcreds
import datetime
import secrets

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST', 'DELETE'])

def gymLoginOut():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_email = request.json.get("email")
        user_password = request.json.get("password")
        rows = None
        user = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user WHERE email = ? AND password = ?", [user_email, user_password])
            user = cursor.fetchall()
            rows = cursor.rowcount
            if(rows == 1):
                loginToken = secrets.token_hex(16)
                cursor.execute("INSERT INTO user_session(userId, loginToken) VALUES(?, ?)", [user[0][1]])   
                conn.commit()
        except Exception as error:
            print(error)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your experience.. oops")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                user_data = {
                    "userId": user[0][1],
                    "email": user[0][3],
                    "username": user[0][1],
                    "goals": user[0][5],
                    "birthdate": user[0][2],
                    "loginToken": loginToken
                }
                return Response(json.dumps(user_data, default = str), mimetype = "application/json", status=201)
            else:
                return Response("Something went really wrong here, try again..", mimetype="text/html", status=500)
    # GYM MEMBER Logout: 
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        userId = request.json.get("loginToken")
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()  
            cursor.execute("DELETE FROM user_session WHERE loginToken = ?", [loginToken])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print(error)
        except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted your experience.. oops")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                return Response("Logout success!", mimetype = "text/html", status=201)
            else:
                return Response("Something went really wrong here, try again..", mimetype="text/html", status=500)

# SIGNUP MEMBER:
@app.route('/api/members', methods=['POST'])
def gymMembers():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_email = request.json.get("email")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_birthdate = request.json.get("birthdate")
        user_goals = request.json.get("goals")
        memberId = request.json.get("memberId")
        rows = None
        user = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor() 
            cursor.execute("INSERT INTO user(email, username, password, birthdate, goals, memberId) VALUES(?, ?, ?, ?, ?, ?)",[user_email, user_username, user_password, user_birthdate, user_goals, memberId]) 
            conn.commit()
            rows = cursor.rowcount
            if rows == 1:
                loginToken = secrets.token_hex(16)
                userId = cursor.lastrowid
                cursor.execute("INSERT INTO user_session(userId, loginToken) VALUES(?, ?)", [userId, loginToken])
                conn.commit()
                rows = cursor.rowcount      
                 except mariadb.ProgrammingError as error:
            print("Something went wrong: Coding error ")        
            print(error)
        except mariadb.OperationalError as error:
            print("uh oh, an Connection error occurred!")
            print(error)
        except mariadb.DatabaseError as error:
            print("A Database error interrupted this.. oops")
            print(error)
        except Exception as error:
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                user_data = {
                    "userId": userId,
                    "email": user_email,
                    "username": user_username,
                    "bio": user_goals,
                    "birthdate": user_birthdate,
                    "loginToken": loginToken
                }
                return Response(json.dumps(user_data, default=str), mimetype="application/json", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)    
