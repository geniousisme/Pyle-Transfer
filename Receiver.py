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

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Receiver(object):
      def __init__(self, recv_ip, recv_port, send_ip, send_port):
          self.recv_sock = init_recv_socket((recv_ip, recv_port))
          self.connections = [self.recv_sock]
          self.recv_ip   = recv_ip
          self.recv_port = recv_port
          self.send_addr = (send_ip, int(send_port))

      def send_open_request(self):
          print "send open request"
          self.recv_sock.sendto("I need a sender~", self.send_addr)

      def receiver_loop(self):
          status = True;
          print "start Pyle Transfer Reciever on %s with port %s ..."          \
                                        % (self.recv_ip, self.recv_port)
          while status:
                try:
                    read_sockets, write_sockets, error_sockets =               \
                                 select.select(self.connections, [], [], 1)
                    if not read_sockets:
                        continue
                    else:
                        send_content, send_addr = self.recv_sock.recvfrom(RECV_BUFFER)
                        print send_content
                        print "receive socket, song!"
                        print "send something back"
                        self.recv_sock.sendto("Hey you sender!", send_addr)

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       status = False
          self.recv_sock.close()

      def run(self):
          self.receiver_loop();

if __name__ == "__main__":
   # addr, port = argv_reader(sys.argv)
   ip, port, send_ip, send_port = localhost, default_port, localhost, default_port + 1
   receiver = Receiver(ip, port, send_ip, send_port)
   receiver.run()