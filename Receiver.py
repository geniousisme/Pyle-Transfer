import os
import select
import socket
import sys

from Utils  import recv_arg_parser
from Utils  import init_recv_socket

from Packet import RECV_BUFFER, HEADER_LENGTH
from Packet import PacketGenerator, PacketExtractor

localhost    = "localhost"#socket.gethostbyname(socket.gethostname())
default_port = 8080

class Receiver(object):
      def __init__(self, recv_ip, recv_port, send_ip, send_port, filename):
          self.recv_sock   = init_recv_socket((recv_ip, recv_port))
          self.connections = [self.recv_sock]
          self.recv_ip     = recv_ip
          self.recv_port   = recv_port
          self.window_size = 1
          self.send_addr   = (send_ip, int(send_port))
          self.file_write  = open(filename, "wb+")
          self.pkt_gen     = PacketGenerator(recv_port, send_port)
          self.pkt_ext     = PacketExtractor(recv_port, send_port)


      def send_open_request(self):
          print "send open request"
          self.recv_sock.sendto("I need a sender~", self.send_addr)

      def send_close_request(self, seq_num, ack_num, fin_flag):
          print "Sending Close Request..."
          packet = self.pkt_gen.generate_packet(seq_num, ack_num, fin_flag)
          self.recv_sock.sendto(packet, self.send_addr)

      def write_file_buffer(self, start_bytes, data_bytes):
          print "write file from %s byte" % start_bytes
          print "data_len:", len(data_bytes)
          # print "data_bytes", data_bytes
          self.file_write.seek(start_bytes)
          self.file_write.write(data_bytes)

      def is_write_file_completed(self):
          return os.path.getsize(self.file_write.name) == self.file_size

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
                        send_packet, send_addr = self.recv_sock.recvfrom       \
                                                 (RECV_BUFFER + HEADER_LENGTH)
                        if "start file tranfer" in send_packet:
                            msg, self.window_size, self.file_size =            \
                                                        send_packet.split(':')
                            self.window_size = int(self.window_size)
                            is_sender_found  = True
                            self.file_size   = int(self.file_size)
                            print "window_size:", self.window_size
                            print "file_size:", self.file_size
                            self.send_addr   = send_addr
                            self.recv_sock.sendto("Come on!", self.send_addr)
                        else:
                            # print "send_packet_len:", len(send_packet)
                            header_params = self.pkt_ext                       \
                                                .get_header_params_from_packet \
                                                                   (send_packet)
                            send_seq_num  = self.pkt_ext                       \
                                                .get_seq_num(header_params)
                            send_ack_num  = self.pkt_ext                       \
                                                .get_ack_num(header_params)
                            send_fin_flag = self.pkt_ext                       \
                                                .get_fin_flag(header_params)
                            if send_fin_flag and self.is_write_file_completed():
                                send_data = self.pkt_ext                       \
                                                .get_data_from_packet          \
                                                          (send_packet)
                                self.write_file_buffer(send_seq_num, send_data)
                                self.send_close_request                        \
                                     (send_seq_num, send_ack_num, send_fin_flag)
                                self.close_receiver()
                                print "Delivery completed successfully"
                            else:
                                send_data = self.pkt_ext                       \
                                                .get_data_from_packet          \
                                                         (send_packet)
                                self.write_file_buffer(send_seq_num, send_data)
                                print "write_file_size:", os.path.getsize(self.file_write.name)
                                seq_num  = send_ack_num
                                ack_num  = send_seq_num                        \
                                           + RECV_BUFFER * self.window_size
                                fin_flag = 0
                                packet = self.pkt_gen                          \
                                             .generate_packet                  \
                                             (seq_num, ack_num, fin_flag)
                                self.recv_sock.sendto(packet, self.send_addr)

                except KeyboardInterrupt, SystemExit:
                       print "\nLeaving Pyle Transfer Receiver..."
                       self.close_receiver()
                       os.remove(self.file_write.name)

          self.recv_sock.close()

      def start_receiver(self):
          self.status = True

      def close_receiver(self):
          self.file_write.close()
          self.status = False

      def run(self):
          self.receiver_loop()

if __name__ == "__main__":
   # addr, port = argv_reader(sys.argv)
   ip, port, send_ip, send_port = localhost, default_port, localhost, default_port + 1
   # params = recv_arg_parser(sys.argv)
   # receiver = Receiver(**params)
   receiver = Receiver(ip, port, send_ip, send_port, "test/received_test.jpeg")
   receiver.run()