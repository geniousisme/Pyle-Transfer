import select
import socket
import sys

from Utils import init_recv_socket
from Utils import RECV_BUFFER

def argv_reader(argv):
    if len(argv) < 3:
       print "receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>"
       print "ex. receiver file.txt 20000 128.59.15.37 20001 logfile.txt"
       sys.exit(1)
    else:
       return argv[1], int(argv[2])

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Receiver(object):
      def __init__(self, recv_ip, recv_port, send_ip, send_port):
          self.recv_sock   = init_recv_socket((recv_ip, recv_port))
          self.connections = [self.recv_sock]
          self.recv_ip     = recv_ip
          self.recv_port   = recv_port
          self.send_addr   = (send_ip, int(send_port))
          self.file_write  = open("received_test.txt", "wb+")
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
          status = True;
          print "start Pyle Transfer Reciever on %s with port %s ..."          \
                                        % (self.recv_ip, self.recv_port)
          is_sender_found = False
          while status:
                try:
                    if not is_sender_found:
                        self.send_open_request()
                    read_sockets, write_sockets, error_sockets =               \
                                 select.select(self.connections, [], [], 1)
                    if not read_sockets:
                        continue
                    else:
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
                                status = False
                                self.file_write.close()
                                print "file delivery completed!"
                            else:
                                self.send_file_request()

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