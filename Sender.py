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
          self.socket_list = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)

      def send_open_response(self):
          self.sender_sock.sendto("lalalala", self.recv_addr)

      def sender_loop(self):
          status = True;
          while status:
                try:
                   recv_msg, recv_addr = self.sender_sock.recvfrom(RECV_BUFFER)
                   print recv_msg
                   status = False
                   # if not read_sockets:
                   #    print "dont receive data yet"
                   #    self.sender_sock.sendto("lalalala", self.recv_addr)
                   # else:
                   #    print "receive receiver data"
                   #    packet_bytes, self.recv_addr = socket.recvfrom(RECV_BUFFER)
                   #    print "Receiver Message:", packet_bytes
                   #    status = False

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.sender_sock.close()

      def run(self):
          self.send_open_response
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   sender  = Sender(ip, port, recv_ip, recv_port)
   sender.run()