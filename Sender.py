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
          self.segment_count = 0
          self.retrans_count = 0

      def retransmit_counter(self):
          self.retrans_count += 1

      def segment_counter(self):
          self.segment_count += 1

      def read_file_buffer(self, start_bytes):
          print "read file from %s byte" % start_bytes
          self.sent_file.seek(start_bytes)
          data_bytes = self.sent_file.read(RECV_BUFFER)
          print "data_bytes", data_bytes
          print "data_len:", len(data_bytes)
          return data_bytes

      def print_transfer_stats(self):
          print "====== Transfering Stats ======="
          print "Total bytes sent:", self.file_size
          print "Segments sent =", 0
          print "Segments Retranmitted =", 0

      def send_file_response(self, *pkt_params):
          packet = self.pkt_gen.generate_packet(*pkt_params)
          self.sender_sock.sendto(packet, self.recv_addr)

      def sender_loop(self):
          self.start_sender()
          is_receiver_found = False
          while self.status:
                try:
                    read_sockets, write_sockets, error_sockets =               \
                                select.select(self.connections, [], [], 1)
                    if read_sockets:
                        recv_packet, recv_addr = self.sender_sock.recvfrom     \
                                                                  (RECV_BUFFER)
                        if recv_packet == "I need a sender~":
                            print "get sender request"
                            self.sender_sock.sendto                            \
                                             ("start file tranfer", recv_addr)
                        elif recv_packet == "Come on!":
                            print "find receiver!!"
                            is_receiver_found = True
                            seq_num = fin_flag = 0 # inital
                            ack_num = RECV_BUFFER
                            self.recv_addr = recv_addr
                            data_bytes = self.read_file_buffer(seq_num)
                            self.send_file_response                            \
                                (seq_num, ack_num, fin_flag, data_bytes)
                        elif is_receiver_found:
                            header_params = self.pkt_ext                       \
                                                .get_header_params_from_packet \
                                                                 (recv_packet)
                            recv_seq_num  = self.pkt_ext                       \
                                                .get_seq_num(header_params)
                            recv_ack_num  = self.pkt_ext                       \
                                                .get_ack_num(header_params)
                            recv_fin_flag = self.pkt_ext                       \
                                                .get_fin_flag(header_params)
                            if recv_fin_flag:
                                print "Delivery completed successfully"
                                self.print_transfer_stats()
                                self.close_sender()
                            else:
                                seq_num  = recv_ack_num
                                ack_num  = recv_seq_num + RECV_BUFFER
                                fin_flag = ack_num >= self.file_size
                                data_bytes = self.read_file_buffer(seq_num)
                                self.send_file_response                        \
                                    (seq_num, ack_num, fin_flag, data_bytes)

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
          self.sender_loop();

if __name__ == "__main__":
   ip, port, recv_ip, recv_port = localhost, default_port + 1, localhost, default_port
   # params = send_arg_parser(sys.argv)
   sender = Sender(ip, port, recv_ip, recv_port, "test/test.pdf")
   sender.run()