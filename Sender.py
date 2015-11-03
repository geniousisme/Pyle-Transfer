import os
import select
import socket
import sys

from Utils import send_arg_parser
from Utils import RECV_BUFFER
from Utils import init_send_socket
from Packet import PacketGenerator, PacketExtractor

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Sender(object):
      def __init__(self, ip, port, recv_ip, recv_port):
          self.sender_sock = init_send_socket((ip, port))
          self.connections = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)
          self.sent_file   = open("test/test.txt", "rb")
          self.status      = None
          self.pkt_gen     = PacketGenerator()
          self.pkt_ext     = PacketExtractor()

      def send_file_response(self, recv_packet):
          start_pos = int(recv_packet.split(':')[1])
          self.sent_file.seek(start_pos)
          read_buffer = self.sent_file.read(RECV_BUFFER)
          self.sender_sock.sendto(read_buffer, self.recv_addr)
          print "send file from %s bytes" % start_pos

      def sender_loop(self):
          self.start_sender()
          while self.status:
                try:
                    read_sockets, write_sockets, error_sockets =                \
                                select.select(self.connections, [], [], 1)
                    if read_sockets:
                        recv_packet, recv_addr = self.sender_sock.recvfrom(RECV_BUFFER)
                        
                        if recv_packet == "I need a sender~":
                            packet = self.pkt_gen.generate_packet()
                            # self.sender_sock.sendto("start file tranfer", recv_addr)
                            self.sender_sock.sendto(packet, recv_addr)

                        elif "start_pos" in recv_packet:
                            file_packet = self.
                            self.send_file_response(recv_packet)
                        else: # close request
                            self.sent_file.close()
                            self.close_sender()

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       self.close_sender()

          self.sender_sock.close()

      def start_sender(self):
          self.status = True

      def close_sender(self):
          self.status = False

      def run(self):
          # self.send_file_response()
          # self.send_open_response()
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   # params = send_arg_parser(sys.argv)
   sender = Sender(ip, port, recv_ip, recv_port)
   sender.run()