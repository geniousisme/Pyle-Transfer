import os
import select
import socket
import sys

from Utils import RECV_BUFFER
from Utils import init_send_socket


def argv_reader(argv):
    if len(argv) < 3:
       print "sender <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename> <window_size>"
       print "ex. sender file.txt 128.59.15.38 20000 20001 logfile.txt 1152"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Sender(object):
      def __init__(self, ip, port, recv_ip, recv_port):
          self.sender_sock = init_send_socket((ip, port))
          self.connections = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)
          self.sent_file   = open("test.txt", "rb")

      def send_open_response(self):
          self.sender_sock.sendto("lalalala", self.recv_addr)

      def send_file_response(self, recv_packet):
          start_pos = int(recv_packet.split(':')[1])
          self.sent_file.seek(start_pos)
          read_buffer = self.sent_file.read(RECV_BUFFER)
          self.sender_sock.sendto(read_buffer, self.recv_addr)
          print "send file from %s bytes" % start_pos

      def sender_loop(self):
          status = True;
          while status:
                try:
                   read_sockets, write_sockets, error_sockets =                \
                                 select.select(self.connections, [], [], 1)
                   if read_sockets:
                      recv_packet, recv_addr = self.sender_sock.recvfrom(RECV_BUFFER)
                      if recv_packet == "I need a sender~":
                         self.sender_sock.sendto("start file tranfer", recv_addr)
                      elif "start_pos" in recv_packet:
                         self.send_file_response(recv_packet)
                      else: # close request
                         self.sent_file.close()
                         status = False

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.sender_sock.close()

      def run(self):
          # self.send_file_response()
          # self.send_open_response()
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   sender  = Sender(ip, port, recv_ip, recv_port)
   sender.run()