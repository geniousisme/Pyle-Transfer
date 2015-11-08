import struct

# ! means network packet, I means short int(2 bytes), H means int(4 bytes)
HEADER_FORMAT = "!HHIIHHHH"
HEADER_LENGTH = 20
RECV_BUFFER   = 20
SORC_PORT_POS = 0
DEST_PORT_POS = 1
SEQ_NUM_POS   = 2
ACK_NUM_POS   = 3
FIN_FLAG_POS  = 4
WINDOW_POS    = 5
CHECKSUM_POS  = 6
URG_PTR_POS   = 7

def calculate_checksum(data_bytes):
    return sum([ord(byte) for byte in data_bytes])


class Packet(object):
    def __init__(self):
        self.sorc_port = 0
        self.dest_port = 0

        self.seq_num  = 0
        self.ack_num  = 0

        self.fin_flag = 0
        self.window   = 0

        self.checksum = 0
        self.urg_ptr  = 0

class UnackedPacket(Packet):
    def __init__(self, ack_num=None, time_stamp=None):
        self.ack_num    = ack_num
        self.begin_time = time_stamp

class PacketExtractor(Packet):
    def __init__(self, sorc_port, dest_port):
        super(PacketExtractor, self).__init__()
        self.sorc_port = sorc_port
        self.dest_port = dest_port

    def get_data_from_packet(self, packet):
        return packet[HEADER_LENGTH:]

    def get_header_params_from_packet(self, packet):
        return struct.unpack(HEADER_FORMAT, packet[:HEADER_LENGTH])

    def get_seq_num(self, header_params):
        return header_params[SEQ_NUM_POS]

    def get_ack_num(self, header_params):
        return header_params[ACK_NUM_POS]

    def get_fin_flag(self, header_params):
        return header_params[FIN_FLAG_POS]

    def get_checksum(self, header_params):
        return header_params[CHECKSUM_POS]

    def is_valid_packet(self, recv_packet): # checksum stuffs
        pass

    def is_checksum_correct(self, checksum):
        pass

class PacketGenerator(Packet):
    def __init__(self, sorc_port, dest_port):
        super(PacketGenerator, self).__init__()
        self.sorc_port = sorc_port
        self.dest_port = dest_port

    def generate_tcp_header(self, seq_num, ack_num, fin_flag):
        self.ack_num  = ack_num
        self.seq_num  = seq_num
        self.fin_flag = fin_flag
        tcp_header = struct.pack(                                             \
                                 HEADER_FORMAT,                               \
                                 self.sorc_port,                              \
                                 self.dest_port,                              \
                                 self.seq_num,                                \
                                 self.ack_num,                                \
                                 self.fin_flag,                               \
                                 self.window,                                 \
                                 self.checksum,                               \
                                 self.urg_ptr                                 \
                                )
        return tcp_header

    def generate_packet(self, seq_num, ack_num, fin_flag, user_data=""):
        return self.generate_tcp_header(seq_num, ack_num, fin_flag) + user_data
