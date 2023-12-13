import socket
import threading
import time

class Transmitter:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.lock = threading.Lock()
        self.connected = False
        self.thread = threading.Thread(target=self.run, daemon=True)

    def connect(self):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.connected = True
                break
            except socket.error as e:
                print(f"Could not connect: {e}")
                self.connected = False
            time.sleep(5)

    def send_message(self, message):
        with self.lock:
            if self.connected:
                try:
                    self.socket.sendall(message.encode())
                except socket.error as e:
                    print(f"Error sending message: {e}")

    def run(self):
        self.connect()
        while self.connected:
            time.sleep(1)

    def start(self):
        self.thread.start()

    def close(self):
        if self.socket:
            self.socket.close()
        self.connected = False