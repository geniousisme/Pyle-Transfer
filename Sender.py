import select
import socket
import sys

from Utils import init_send_packet

def argv_reader(argv):
    if len(argv) < 3:
       print "Usage: python client.py hostname port"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])


class Sender(object):
      def __init__(self, host, port):
          self.sender_sock = socket(AF_INET, SOCK_DGRAM)
          self.socket_list = [sys.stdin, self.sender_sock]

      def sender_loop(self):
          status = True;

          while status:
                try:
                   read_sockets, write_sockets, error_sockets =            \
                                 select.select(self.socket_list, [], [], 1)

                   for socket in read_sockets:
                       if socket is self.server_connect: # msg from server
                          msg = socket.recv(RECV_BUFFER)


                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.server_connect.close()

      def run(self):
          self.sender_loop();

if __name__ == "__main__":
   host, port = argv_reader(sys.argv)
   client     = Client(host, port)
   client.run()