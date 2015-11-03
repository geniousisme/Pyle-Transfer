import os
import select
import socket
import sys

from Utils import send_arg_parser
from Utils import init_send_socket

from Packet import RECV_BUFFER
from Packet import PacketGenerator, PacketExtractor

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Sender(object):
      def __init__(self, send_ip, send_port, recv_ip, recv_port, filename):
          self.sender_sock = init_send_socket((send_ip, send_port))
          self.connections = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)
          self.sent_file   = open(filename, "rb")
          self.file_size   = os.path.getsize(filename)
          self.status      = None
          self.pkt_gen     = PacketGenerator(send_port, recv_port)
          self.pkt_ext     = PacketExtractor(send_port, recv_port)

      # def send_file_response(self, recv_packet):
      #     start_pos = int(recv_packet.split(':')[1])
      #     self.sent_file.seek(start_pos)
      #     read_buffer = self.sent_file.read(RECV_BUFFER)
      #     self.sender_sock.sendto(read_buffer, self.recv_addr)
      #     print "send file from %s bytes" % start_pos

      def read_file_buffer(self, start_bytes):
          print "read file from %s byte" % start_bytes
          self.sent_file.seek(start_bytes)
          data_bytes = self.sent_file.read(RECV_BUFFER)
          # print data_bytes
          print "data_len:", len(data_bytes)
          return data_bytes

      def print_transfer_stats(self):
          print "Delivery Completed Successfully."
          print "====== Transfering Stats ======="
          print "Total bytes sent:", self.file_size
          print "Segments sent =", 0
          print "Segments Retranmitted =", 0

      def sender_loop(self):
          self.start_sender()
          is_receiver_found = False
          while self.status:
                try:
                    read_sockets, write_sockets, error_sockets =                \
                                select.select(self.connections, [], [], 1)
                    if read_sockets:
                        recv_packet, recv_addr = self.sender_sock.recvfrom(RECV_BUFFER)
                        if recv_packet == "I need a sender~":
                            print "get sender request"
                            # packet = self.pkt_gen.generate_packet()
                            self.sender_sock.sendto("start file tranfer", recv_addr)
                            # self.sender_sock.sendto(packet, recv_addr)
                        elif recv_packet == "Come on!":
                            print "find receiver!!"
                            is_receiver_found = True
                            seq_num = ack_num = fin_flag = 0 # inital
                            file_data_bytes = self.read_file_buffer(seq_num)
                            packet = self.pkt_gen.generate_packet(seq_num, ack_num, fin_flag, file_data_bytes)
                            print "send_packet_len", len(packet)
                            self.sender_sock.sendto(packet, recv_addr)
                        elif is_receiver_found:
                            header_params = self.pkt_ext.get_header_params_from_packet(recv_packet)
                            # recv_data     = self.pkt_ext.get_header_from_packet(recv_packet)
                            recv_seq_num  = self.pkt_ext.get_seq_num(header_params)
                            recv_ack_num  = self.pkt_ext.get_ack_num(header_params)
                            recv_fin_flag = self.pkt_ext.get_fin_flag(header_params)
                            if recv_fin_flag:
                                self.print_transfer_stats()
                                self.close_sender()
                                print "Delivery Completed!"
                            else:
                                seq_num  = recv_ack_num
                                ack_num  = recv_seq_num + RECV_BUFFER
                                fin_flag = ack_num >= self.file_size
                                file_data_bytes = self.read_file_buffer(seq_num)
                                packet = self.pkt_gen.generate_packet(seq_num, ack_num, fin_flag, file_data_bytes)
                                print "send_packet_len", len(packet)
                                self.sender_sock.sendto(packet, recv_addr)

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer..."
                       self.close_sender()

          self.sender_sock.close()

      def start_sender(self):
          self.status = True

      def close_sender(self):
          self.sent_file.close()
          self.status = False

      def run(self):
          # self.send_file_response()
          # self.send_open_response()
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   # params = send_arg_parser(sys.argv)
   sender = Sender(ip, port, recv_ip, recv_port, "test/test.pdf")
   sender.run()