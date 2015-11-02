import select
import socket
import sys

from Utils import recv_arg_parser
from Utils import init_recv_socket
from Utils import RECV_BUFFER

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Receiver(object):
      def __init__(self, recv_ip, recv_port, send_ip, send_port):
          self.recv_sock   = init_recv_socket((recv_ip, recv_port))
          self.connections = [self.recv_sock]
          self.recv_ip     = recv_ip
          self.recv_port   = recv_port
          self.send_addr   = (send_ip, int(send_port))
          self.file_write  = open("test/received_test.txt", "wb+")
          self.start_pos   = 0

      def send_open_request(self):
          print "send open request"
          self.recv_sock.sendto("I need a sender~", self.send_addr)

      def read_file_response(self, send_packet):
          print "write file from %s byte" % self.start_pos
          self.file_write.seek(self.start_pos)
          self.file_write.write(send_packet)
          self.start_pos += RECV_BUFFER

      def send_file_request(self):
          self.recv_sock.sendto("start_pos:" + str(self.start_pos), self.send_addr)
          print "request file from %s byte" % self.start_pos

      def send_close_request(self):
          self.recv_sock.sendto("Done!!!", self.send_addr)

      def receiver_loop(self):
          self.start_receiver()
          print "start Pyle Transfer Reciever on %s with port %s ..."          \
                                        % (self.recv_ip, self.recv_port)
          is_sender_found = False
          while self.status:
                try:
                    if not is_sender_found:
                        self.send_open_request()
                    read_sockets, write_sockets, error_sockets =               \
                                 select.select(self.connections, [], [], 1)
                    if read_sockets:
                        send_packet, send_addr = self.recv_sock.recvfrom(RECV_BUFFER)
                        if not is_sender_found:
                            is_sender_found = True
                            self.send_addr = send_addr
                        if send_packet == "start file tranfer":
                            self.send_file_request()
                        else:
                            self.read_file_response(send_packet)
                            if self.start_pos + RECV_BUFFER >= 113:
                                self.send_close_request()
                                self.file_write.close()
                                self.close_receiver()
                                print "file delivery completed!"
                            else:
                                self.send_file_request()

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       self.close_receiver()
                       os.remove(self.file_write.name)

          self.recv_sock.close()

      def start_receiver(self):
          self.status = True

      def close_receiver(self):
          self.status = False

      def run(self):
          self.receiver_loop()

if __name__ == "__main__":
   # addr, port = argv_reader(sys.argv)
   params = localhost, default_port, localhost, default_port + 1
   # params = recv_arg_parser(sys.argv)
   # receiver = Receiver(**params)
   receiver = Receiver(ip, port, send_ip, send_port)
   receiver.run()