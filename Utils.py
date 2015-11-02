import datetime
import os
import socket
import sys


RECV_BUFFER     = 576

def recv_arg_parser(argv):
    print "here is receiver parser"

def send_arg_parser(argv):
    print "here is sender parser"


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