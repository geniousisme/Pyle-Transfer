import logging
import os
import select
import socket
import sys
import time

from Utils import send_arg_parser
from Utils import init_send_socket

from Packet import RECV_BUFFER, calculate_checksum
from Packet import PacketGenerator, PacketExtractor, UnackedPacket

TIME_OUT     = 0.5 # sec
localhost    = socket.gethostbyname(socket.gethostname())
default_port = 8080

class Sender(object):
      def __init__(self, send_ip, send_port, recv_ip, recv_port,
                   filename, window_size=1):
          self.sender_sock = init_send_socket((send_ip, send_port))
          self.connections = [self.sender_sock]
          self.recv_addr   = (recv_ip, recv_port)
          self.sent_file   = open(filename, "rb")
          self.file_size   = os.path.getsize(filename)
          self.window_size = window_size
          self.status      = None
          self.pkt_gen     = PacketGenerator(send_port, recv_port)
          self.pkt_ext     = PacketExtractor(send_port, recv_port)
          self.segment_count  = 0
          self.retrans_count  = 0
          self.oldest_unacked_pkt = UnackedPacket()

          self.logger = logging.getLogger("Sender")
          self.logger.setLevel(logging.INFO)

          hd        = logging.StreamHandler()
          formatter = logging.                                                 \
                      Formatter                                                \
                      ("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

          hd.setFormatter(formatter)
          self.logger.addHandler(hd)

      def retransmit_counter(self):
          self.retrans_count += 1

      def segment_counter(self):
          self.segment_count += 1

      def read_file_buffer(self, start_bytes):
          self.logger.debug("read file from %s byte" % start_bytes)
          self.sent_file.seek(start_bytes)
          data_bytes = self.sent_file.read(RECV_BUFFER)
          self.logger.debug("data_len: %s bytes" % len(data_bytes))
          return data_bytes

      def print_transfer_stats(self):
          print "====== Transfering Stats ======="
          print "Total bytes sent:", self.file_size
          print "Segments sent =", self.segment_count
          print "Segments Retranmitted =", self.retrans_count

      def send_file_response(self, *pkt_params):
          self.segment_counter()
          packet = self.pkt_gen.generate_packet(*pkt_params)
          self.logger.debug("checksum: %s" % calculate_checksum(*pkt_params))
          self.sender_sock.sendto(packet, self.recv_addr)

      def send_initial_file_response(self):
          for i in xrange(self.window_size):
             seq_num = i * RECV_BUFFER
             ack_num = seq_num + self.window_size * RECV_BUFFER
             if i == 0:
                self.oldest_unacked_pkt.ack_num = ack_num
                self.oldest_unacked_pkt.begin_time = time.time()
             data_bytes = self.read_file_buffer(seq_num)
             fin_flag = len(data_bytes) == 0
             if fin_flag:
                # means we already send all of data at initial stage,
                # dont need to tranfer the rest of packet.
                break
             self.send_file_response(seq_num, ack_num, fin_flag, data_bytes)

      def retransmit_file_response(self):
          self.logger.debug("retransmit!!!")
          self.logger.debug                                                    \
          ("oldest_unacked_pkt: %s" % self.oldest_unacked_pkt.ack_num)
          initial_seq =                                                        \
            self.oldest_unacked_pkt.ack_num - self.window_size * RECV_BUFFER
          for i in xrange(self.window_size):
             self.retransmit_counter()
             seq_num = initial_seq + i * RECV_BUFFER
             self.logger.debug("retransmit_seq_num: %s" % seq_num)
             ack_num = seq_num + self.window_size * RECV_BUFFER
             self.logger.debug("retransmit_ack_num: %s" % ack_num)
             if i == 0:
                self.oldest_unacked_pkt.ack_num = ack_num
                self.oldest_unacked_pkt.begin_time = time.time()
             data_bytes = self.read_file_buffer(seq_num)
             fin_flag = len(data_bytes) == 0
             self.send_file_response(seq_num, ack_num, fin_flag, data_bytes)

      def is_oldest_unacked_pkt_timeout(self):
          if self.oldest_unacked_pkt.begin_time is None:
            return False
          return time.time() - self.oldest_unacked_pkt.begin_time >= TIME_OUT

      def sender_loop(self):
          self.start_sender()
          is_receiver_found = False
          while self.status:
                try:
                    if self.is_oldest_unacked_pkt_timeout():
                        self.logger.debug("timeout!")
                        self.retransmit_file_response()
                    read_sockets, write_sockets, error_sockets =               \
                                select.select(self.connections, [], [], 1)
                    if read_sockets:
                        recv_packet, recv_addr = self.sender_sock.recvfrom     \
                                                                  (RECV_BUFFER)
                        if recv_packet == "I need a sender~":
                            self.sender_sock.sendto                            \
                                ("start file tranfer:%s:%s" %                  \
                                (self.window_size, self.file_size),            \
                                 recv_addr)

                        elif recv_packet == "Come on!":
                            is_receiver_found = True
                            self.send_initial_file_response()

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
                                if self.oldest_unacked_pkt.ack_num == recv_seq_num:
                                    seq_num  = recv_ack_num
                                    ack_num  = recv_seq_num                    \
                                               + RECV_BUFFER * self.window_size
                                    fin_flag = ack_num >= self.file_size
                                    data_bytes = self.read_file_buffer(seq_num)
                                    self.send_file_response                    \
                                        (seq_num, ack_num, fin_flag, data_bytes)
                                    self.oldest_unacked_pkt.ack_num += RECV_BUFFER
                                    self.oldest_unacked_pkt.begin_time = time.time()
                                else:
                                    self.logger.debug("expected_ack not correct !!!")
                                    self.logger.debug("oldest_unacked_pkt.num: %s" % self.oldest_unacked_pkt.ack_num)
                                    self.logger.debug("recv_seq_num: %s, ignore" % recv_seq_num)
                                # else, ignore the packet

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
   ip, port, recv_ip, recv_port = localhost, default_port, localhost, 41192
   params = send_arg_parser(sys.argv)
   sender = Sender(ip, port, recv_ip, recv_port, "test/test.pdf", 1000)
   sender.run()
   # 160.39.227.140 with port 8082