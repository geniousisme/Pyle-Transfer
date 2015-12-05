# Pyle-Transfer
### Computer Networks Programming Assignment 2: UDP File Transfer

![Hope you like it](http://www.quickmeme.com/img/2a/2a78d6fdba8442a5e63b39d5dd283d142ad7208f07af03a6d7beaa82835dbe32.jpg)


#### Program Overview
------

This program implements a TCP-like protocol on top of UDP. It support variable window size, and can recover from data loss, data corruption, and data delay. Basically, I implement the TCP 20 bytes header as follow:

[ Source port ][ Dest port  ]
[     Sequence Number       ]
[  Acknowledgement Number   ]
[  Flags    ][Receive window]
[ Checksum  ][  Urgent ptr  ]
[ Data Data Data Data  .... ]

I use timeout mechanism to prevent the dealy, and use checksum to check if the packer is cirrupted, and use ack number & sequence number to check if the packet id inorder or not. For supporting the variable window size, I implement GBN mechanism in my program.

#### Code Description
------

Pyle-Tranfer includes 4 files:

- main program files: Utils.py, Packet.py, receiver.py, sender.py

1. Utils.py:

  Implement several handy utility function in this file. Like progress_bar,
  argv parser, and socket initialization.

2. Packet.py

  Packet.py contains PacketGenerator and PacketExtractor, PacketGenerator is to
  generate packet, including headers and data; PacketExtractor is responsible for
  extracting the information in the packet, and also checking checksum of the packet.

3. receiver.py

  Collect the sender's datagram packet, checks for corrupted information and
  that the received packet is in-order or not. If there is something wrong, then it will ignore the packets and following packets, and then wait for the retransmission from sender.

4. sender.py:

  Read from the file and sends the data bytes to the designated receiver.
  And it will waits for the corresponding ACK response before continuing in the transmission process. If no such ACKs during the time period, the Sender will retransmit the packet.

For the log_filename, if it is stdout, it will log to stdout.

- other files: Makefile.

1. Makefile: nothing there, just some echo message.

#### How to use it?
------

To run the program:

1. Start the receiver.py with the port number that you want to use, and also other parameters:

*python receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>

2. Start the sender.py:

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

#### Extra Feature:
------
1. Integrate logging module into this program, if you want to see the effect you can add "debug" at the end of commands for invoking sender or receiver, then you can feel the strength of logging module

2. Progrss bar implementation:
Since there is nothing to see when receiver is receiving things, which is borning and confusing, especially when you use high error rate, high delay time, or high data loss to test your code. So I think if I have a prgress bar on my receiver side then I can know how the progress goes.

It will looks like this when receiver is receiving the file from sender:

File Delivering...[==============                                    ] 29%

Remember to widen your terminal more than 80 pixel, or it will look funny.
------

#### Hope you enjoy Pyle-Transfer !!!

=======
