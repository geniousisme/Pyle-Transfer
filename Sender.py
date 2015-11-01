import os
import select
import socket
import sys

from Utils import RECV_BUFFER
from Utils import init_send_socket


def argv_reader(argv):
    if len(argv) < 3:
       print "Usage: python client.py hostname port"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Sender(object):
      def __init__(self, ip, port, recv_ip, recv_port):
          self.sender_sock = init_send_socket()
          self.connections = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)

      def send_open_response(self):
          self.sender_sock.sendto("lalalala", self.recv_addr)

      def send_file_response(self):
          sent_file = open("test.pdf", "rb")
          print "file_size:", os.path.getsize("test.pdf")
          read_buffer = sent_file.read(RECV_BUFFER)
          self.sender_sock.sendto(read_buffer, self.recv_addr)
          print "send the test file to receiver!"

      def sender_loop(self):
          status = True;
          while status:
                try:
                   read_sockets, write_sockets, error_sockets =                \
                                 select.select(self.connections, [], [], 1)
                   if read_sockets:
                      recv_packet, recv_addr = self.sender_sock.recvfrom(RECV_BUFFER)
                      print recv_packet
                      status = False

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.sender_sock.close()

      def run(self):
          self.send_file_response()
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   sender  = Sender(ip, port, recv_ip, recv_port)
   sender.run()