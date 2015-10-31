import select
import socket
import sys

from Utils import init_recv_socket
from Utils import RECV_BUFFER

def argv_reader(argv):
    if len(argv) < 3:
       print "receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])

localhost    = socket.gethostbyname(socket.gethostname())
default_port = 8080

class Receiver(object):
      def __init__(self, addr, port):
          self.recv_sock = init_recv_socket((addr, port))
          self.connections = [self.recv_sock]
          self.recv_addr = addr
          self.recv_port = port

      def receiver_loop(self):
          status = True;
          print "start Pyle Transfer Reciever on %s with port %s ..." % (self.recv_addr, self.recv_port)
          while status:
                try:
                   read_sockets, write_sockets, error_sockets =            \
                                 select.select(self.connections, [], [], 1)

                   for socket in read_sockets:
                       if socket is self.recv_sock: # msg from server
                          print "it is receiver self socket."
                       else: # msg from user to type in
                          print "it is sender socket, yeah!"
                          status = False

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.recv_sock.close()

      def run(self):
          self.receiver_loop();

if __name__ == "__main__":
   # addr, port = argv_reader(sys.argv)
   addr, port = localhost, default_port
   receiver   = Receiver(addr, port)
   receiver.run()