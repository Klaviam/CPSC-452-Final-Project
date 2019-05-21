# To get pymysql, use pip install pymysql
import pymysql
import importlib
import client

def main():
    print "\nWELCOME TO CHAT 1.0\n"

    choice = raw_input("Login or register? ").upper()

    isRegistered = False

    if choice == "REGISTER" or choice.upper() == "R":
        print "\nREGISTRATION:"
        client.Register()
        isRegistered = True

    if choice == "LOGIN" or choice.upper() == "L" or isRegistered:
        print "\nLOGIN:"
        username = raw_input("Enter your username: ")
        password = raw_input("Enter your password: ")

        # Server verifies user/pass, if true, then set this user's activity to "Online"
        isValid = client.Validate(username, password)

        if isValid == "true":
            print "\nWelcome " + username + "!"

            isExitting = False

            # Get list of users
            UsersOnline(username)
            print "Type '!help' to see a list of commands.\n"

            while not isExitting:
                command = raw_input("Enter command: ")

                db = pymysql.connect("localhost", "", "", "chat")
                cursor = db.cursor()
# Invite
                if command[0:7] == "!invite":
                    inviteCommand = command.split(" ")

                    if len(inviteCommand) == 3:
                        db = pymysql.connect("localhost", "", "", "chat")
                        cursor = db.cursor()
                        cursor.execute("SELECT username FROM users WHERE username = '{0}'".format(inviteCommand[1]))
                        result = cursor.fetchone()

                        if result:
                            if result[0] != username:
                                cursor.execute("SELECT status FROM users WHERE username = '{0}'".format(inviteCommand[1]))
                                status = cursor.fetchone()
                                if status[0] == "Online":
                                    if inviteCommand[2].upper() == "RSA" or inviteCommand[2].upper() == "DSA":
                                        Invite(username, inviteCommand[1], inviteCommand[2])
                                    else:
                                        print "\nERROR - Use either the 'RSA' or 'DSA' algorithms!\n"
                                else:
                                    print "\nERROR - " + result[0] + " is not online at the moment!\n"
                            else:
                                print "\nERROR - You cannot invite yourself!\n"
                        else:
                            print "\nERROR - Cannot find " + inviteCommand[1] + "!\n"
                    else:
                        print "\nERROR - Invite using the form '!invite <name> <RSA/DSA>'!\n"
# Help
                elif command == "!help":
                    print ( "\nCOMMANDS\n" +
                            "'!invite <name> <RSA/DSA>' will open a chat with that person using either RSA or DSA.\n" +
                            "'!users' will list all the registered users.\n" +
                            "'!refresh' will reset all user's statuses to 'Offline'.\n" +
                            "'!exit' will quit the program.\n")
# Users
                elif command == "!users":
                    UsersOnline(username)
# Refresh
                elif command == "!refresh":
                    Refresh(username)
# Exit
                elif command == "!exit":
                    print "\nExiting chatroom. See ya!\n"
                    isExitting = True
                    # Set status to Offline
                    cursor.execute("UPDATE users SET status = 'Offline' WHERE username = '{0}'".format(username))
                    db.commit()
                else:
                    print "\nERROR - Invalid command! Type '!help' to see a list of commands\n"
        else:
            print "\n" + isValid


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


# Resets all statuses in case someone exitted without logging out (CAUTION: Use with care!)
def Refresh(username):
    print "\nRefreshed all users.\n"

    db = pymysql.connect("localhost", "", "", "chat")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET status = 'Offline'")
    db.commit()

    cursor.execute("UPDATE users SET status = 'Online' WHERE username = '{0}'".format(username))
    db.commit()

    db.close()


# Connects to another user
def Invite(myUsername, theirUsername, alg):
    print "\nInviting " + theirUsername + " using " + alg.upper() + "...\n"
    client.ChatSession(myUsername, theirUsername, alg)


if __name__== "__main__":
  main()
