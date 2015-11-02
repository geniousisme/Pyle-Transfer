import datetime
import os
import socket
import sys


RECV_BUFFER     = 576

def recv_arg_parser(argv):
    if len(argv) < 6:
       print "length of arguments is not enough."
       print "format: receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>"
       print "ex. receiver.py file.txt 20000 128.59.15.37 20001 logfile.txt"
       sys.exit(1)
    else:
       return {
               "filename": argv[1],                                             \
               "recv_port": int(argv[2]),                                       \
               "send_ip": argv[3],                                              \
               "send_port": int(argv[4]),                                       \
               "log_filename": argv[5]                                          \
              }

def send_arg_parser(argv):
    if len(argv) < 7:
       print "length of arguments is not enough."
       print "sender <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename> <window_size>"
       print "ex. sender file.txt 128.59.15.38 20000 20001 logfile.txt 1152"
       sys.exit(1)
    else:
       return {
               "filename"    : argv[1],                                         \
               "recv_ip"     : argv[2],                                         \
               "recv_port"   : int(argv[3]),                                    \
               "send_port"   : int(argv[4]),                                    \
               "log_filename": argv[5]                                          \
               "window_size" : int(argv[6])                                     \
              }

def init_recv_socket(address):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(address)
    udp_socket.setblocking(True)
    return udp_socket

def init_send_socket(address):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(address)
    udp_socket.setblocking(True)
    return udp_socket