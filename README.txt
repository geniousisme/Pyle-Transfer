PyTalk
Computer Networks Programming Assignment 2: Socket Programming - Simple Chat App

Chia-Hao Hsu
UNI: ch3141

------------------------------- Description -----------------------------------

PyTalk includes 6 files:

main program files: user_pass.txt, utils.py, client.py, server.py

utils.py: class for utility function
          Like message parser, connecting server,
          and all the variable(TIME_OUT, BLOCK_TIME, etc...)
          that would be used in server and client.

user.py: class for every PyTalk user of the chat room.
         It defines a user that has a username, socket, ip,
         and its active_time allow us to use user object
         directly to do several things without confusion.

client.py: class for PyTalk client side. Basically client doesn't do
            too many complicated things. It just receive the message
            sent from server, and make the move(ex. send message or
            exit PyTalk) with different message.

server.py: class for PyTalk server side. Server will recieve all
           the message sent from client. It will decide the client
           login sucessfully or not(and is user repeated or need to
           block too), and what kind of messag client send and decide
           what kind of action to do with different income message.

other files: user_pass.txt, Makefile.

user_pass.txt: has all the credentials to access the chat.
Makefile: nothing there, just some echo message.

------------------------------- How to use it ---------------------------------

To run the program:
    1. Start the server with the port number that you want to user.
        python Server.py port_number
    2. Start the client with the ip number provided by the server and the same
       port number.
        python Client.py server_ip port_number

Implemented commands:

commands                        Functionality
whoelse                         Displays name of other connected users
wholast [number]                Displays name of those users
                                connected within the last [number] minutes. Let 0 < number < 60|
broadcast message [message]     Broadcasts [message] to all connected users
broadcast user [user] [user]... Broadcasts [message] to the list of users
[user] message [message]
message [user] [message]        Private [message] to a [user]
logout                          Log out this user.

