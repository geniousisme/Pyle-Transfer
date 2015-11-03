import 
import struct

class PacketExtractor(object):
    def __init__(self):
        self.ack_num = 0
        self.seq_num = 0
        self.sorc_port = 0
        self.dest_port = 0
        self.checksum  = 0
        self.window_size = 0

    def generate_tcp_header(self):
        pass

    def generate_packet(self, header, data):
        return header + data

class PacketGenerator(object):
    def __init__(self):
        self.ack_num = 0
        self.seq_num = 0
        self.sorc_port = 0
        self.dest_port = 0
        self.checksum  = 0
        self.window_size = 0

    def generate_tcp_header(self):
        pass

    def generate_packet(self, header, data):
        return header + data



