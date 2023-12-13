import socket

IP = '127.0.0.1'
PORT = 20001


def receiver(): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((IP, PORT))
        s.listen()
        print(f"Server listening on {IP}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")

if __name__ == '__main__':
    receiver()