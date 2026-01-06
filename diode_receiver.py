# diode_receiver.py
# Runs on IT side to receive unidirectional data
# Cannot send anything back to OT (hardware prevents it)

import socket
import json
import sqlite3
from datetime import datetime

class DiodeReceiver:
    """Receive data from unidirectional gateway and store in historian"""

    def __init__(self, listen_port, db_path='historian.db'):
        self.listen_port = listen_port
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize historian database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS process_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                source TEXT,
                tag_name TEXT,
                value REAL,
                received_at TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def store_data(self, payload):
        """Store received data in historian database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Store PLC data
        for plc_name, tags in payload.get('plc_data', {}).items():
            for tag_name, value in tags.items():
                cursor.execute('''
                    INSERT INTO process_data (timestamp, source, tag_name, value, received_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (payload['timestamp'], plc_name, tag_name, value, datetime.now().isoformat()))

        # Store OPC data
        for opc_name, nodes in payload.get('opc_data', {}).items():
            for node_id, value in nodes.items():
                cursor.execute('''
                    INSERT INTO process_data (timestamp, source, tag_name, value, received_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (payload['timestamp'], opc_name, node_id, value, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def listen(self):
        """Listen for UDP data from diode"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', self.listen_port))

        print(f"Listening for data from diode on port {self.listen_port}...")

        while True:
            try:
                data, addr = sock.recvfrom(65535)  # Max UDP packet size
                payload = json.loads(data.decode('utf-8'))

                self.store_data(payload)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received data from {payload['source']}")

            except Exception as e:
                print(f"Error receiving data: {e}")

# Usage
if __name__ == '__main__':
    receiver = DiodeReceiver(listen_port=5000)
    receiver.listen()
