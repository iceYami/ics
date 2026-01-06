# Example: Identify packet structure
def find_preamble(bits, preamble="10101010"):
    preamble_bits = [int(b) for b in preamble]
    matches = []

    for i in range(len(bits) - len(preamble_bits)):
        if list(bits[i:i+len(preamble_bits)]) == preamble_bits:
            matches.append(i)

    return matches

# Find packets
packets = find_preamble(bits)
print(f"Found {len(packets)} potential packets")

# Extract first packet
if packets:
    packet_start = packets[0]
    packet_bits = bits[packet_start:packet_start+200]  # Assume 200-bit packet
    print(f"Packet bits: {packet_bits}")
