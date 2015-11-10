# Pyle-Transfer
### Computer Networks Programming Assignment 2: UDP File Transfer

#### Program Overview
------

This program implements a TCP-like protocol on top of UDP. It support variable window size, and can recover from data loss, data corruption, and data delay. Basically, I implement the TCP 20 bytes header as follow:

[ Source port ][ Dest port  ]
[     Sequence Number       ]
[  Acknowledgement Number   ]
[  Flags    ][Receive window]
[ Checksum  ][  Urgent ptr  ]
[ Data Data Data Data  .... ]


#### Code Description
------

The receiver is invoked, self-explanatorily, using
./receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>

The sender is invoked with
./sender.py <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename>

For the log_filename, if it is stdout, it will log to stdout.

The sender additionally logs the estimated RTT in seconds every time it receives an ACK (which is when it calculates a new value). 

Pyle-Tranfer includes 4 files:

- main program files: Utils.py, Packet.py, receiver.py, sender.py

1. Utils.py:

  class for utility function
  Like message parser, connecting server,
  and all the variable(TIME_OUT, BLOCK_TIME, etc...)
  that would be used in server and client.

2. user.py:

  class for every PyTalk user of the chat room.
  It defines a user that has a username, socket, ip,
  and its active_time allow us to use user object
  directly to do several things without confusion.

3. client.py:

  class for PyTalk client side. Basically client doesn't do
  too many complicated things. It just receive the message
  sent from server, and make the move(ex. send message or
  exit PyTalk) with different message.

4. Sender.py:

  class for PyTalk server side. Server will recieve all
  the message sent from client. It will decide the client
  login sucessfully or not(and is user repeated or need to
  block too), and what kind of messag client send and decide
  what kind of action to do with different income message.

- other files: Makefile.

1. Makefile: nothing there, just some echo message.

#### How to use it?
------

To run the program:

1. Start the receiver.py with the port number that you want to use, and also other parameters:

*python receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>

2. Start the sender.py with the ip number provided by the server and the same port number.

*python sender.py <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename> <window_size>

#### How do I test it?
------

I use Proxy provided by TA, use following command to test my program:

0. start the proxy emulator:
./newudpl -i192.168.0.3:8080 -o192.168.0.3:8082 -B30000 -L50 -O30 -d0.6

1. invoke receiver:
python Receiver.py test/received.pdf 8082 192.168.0.3 8080 log/recv_log.txt

2. invoke sender:
python Sender.py test/test.pdf 192.168.0.3 41192 8080 log/send_log.txt 1000

No matter in data loss situation, data corrupted, or data delay situation,
my program can always recover from the situations.


#### Hope you enjoy Pyle-Transfer !!!
![Hope you like it](http://cdn0.vox-cdn.com/assets/5057232/kerley_dance.gif)

=======
