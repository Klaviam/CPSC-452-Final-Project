import socket
import pymysql
import importlib
import address
import select
import sys
import time
import address
import hashlib, uuid

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return reduce(lambda x,y:x+y, lst)
def Register():
    isTaken = False

    while not isTaken:
        username = raw_input("Username: ")

        # Check if username is taken
        db = pymysql.connect("localhost", "", "", "chat")
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users")
        usersResult = cursor.fetchall()

        isTaken = True
        for i in range(len(usersResult)):
            if usersResult[i][0] == username:
                print "\nERROR - Username already taken!\n"
                isTaken = False
        if not isTaken:
            username = raw_input("Username: ")

    password = raw_input("Password: ")

    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address.HOST, address.PORT))

    s.sendall("register " + " " + username + " " + str(hashed_password))
    data = s.recv(1024)

    cursor.execute("UPDATE users SET salt = '{0}' WHERE username = '{1}'".format(salt, username))
    db.commit()

    s.close()

def Validate(username, password):

    # Get user's salt value and rehash password
    db = pymysql.connect("localhost", "", "", "chat")
    cursor = db.cursor()
    cursor.execute("SELECT salt FROM users WHERE username = '{0}'".format(username))
    result = cursor.fetchone()

    hashed_password = ""
    if result:
        salt = str(result[0])

        hashed_password = hashlib.sha512(password + salt).hexdigest()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address.HOST, address.PORT))

    s.sendall("validate " + " " + username + " " + hashed_password)
    data = s.recv(1024)

    s.close()
    db.close()

    return data


def ChatSession(myUsername, theirUsername, alg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address.HOST, address.PORT))

    s.sendall("message")

    print "CHATROOM:"
    print "You and " + theirUsername + " have joined the chatroom!\n"

    isExitting = False

    while not isExitting:
        sockets_list = [sys.stdin, s]
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == s:
                time.sleep(.1)
                message = socks.recv(2048)
                if message != "message":
                    print message
            else:
                message = raw_input("")
        # View user list
                if message == "!users":
                    UsersOnline(myUsername)
        # View help
                elif message == "!help":
                    print ( "\nCOMMANDS\n" +
                            "'!users' will list all the registered users.\n" +
                            "'!exit' will leave the chatroom.\n")
        # Exit chatroom
                elif message == "!exit":
                    print "\nLeaving the chatroom...\n"
                    isExitting = True
                    s.send(message)
        # Send message
                else:
                    s.send(message)
    time.sleep(.1)
    s.close()



# Prints users online and their status
def UsersOnline(myUsername):
    db = pymysql.connect("localhost", "", "", "chat")
    cursor = db.cursor()

    cursor.execute("SELECT username FROM users")
    usersResult = cursor.fetchall()

    cursor.execute("SELECT status FROM users")
    statusResult = cursor.fetchall()

    offlineUsers = []

    print "\nOFFLINE USERS:"
    for i in range(len(usersResult)):
        if usersResult[i][0] != myUsername:
            if statusResult[i][0] == "Offline":
                print usersResult[i][0]
            else:
                offlineUsers.append(usersResult[i][0])
    print "\nONLINE USERS: \n" + "\n".join(offlineUsers) + "\n"
    db.close()
