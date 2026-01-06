from boofuzz import *

def main():
    # Define S7comm protocol
    s_initialize("s7comm_cotp_cr")

    # TPKT Header
    s_static("\x03\x00")  # Version, Reserved
    s_size("tpkt_length", offset=0, length=2, endian=">", fuzzable=False)

    if s_block_start("tpkt_length"):
        # COTP Connection Request
        s_byte(0x11, name="cotp_length", fuzzable=True)
        s_byte(0xE0, name="cotp_pdu_type", fuzzable=True)  # CR
        s_word(0x0000, name="dest_ref", endian=">", fuzzable=True)
        s_word(0x0001, name="src_ref", endian=">", fuzzable=True)
        s_byte(0x00, name="class_option", fuzzable=True)

        # Parameters
        s_byte(0xC1, name="param1", fuzzable=True)
        s_byte(0x02, name="param1_len", fuzzable=False)
        s_word(0x0100, name="tpdu_size", endian=">", fuzzable=True)

    s_block_end("tpkt_length")

    # Setup session
    session = Session(target=Target(connection=SocketConnection("192.168.1.100", 102, proto="tcp")))

    session.connect(s_get("s7comm_cotp_cr"))

    # Fuzz!
    session.fuzz()

if __name__ == "__main__":
    main()
