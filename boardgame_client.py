# boardgame_client.py
import socket
import threading

def listen_for_server(sock):
    while True:
        try:
            message = sock.recv(16384).decode('utf-8')
            if not message:
                break
            print("\n" + message)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client.connect(('10.233.202.156', 12345)) # hotspot
    client.connect(('127.0.0.1', 50000))  # local machine

    threading.Thread(target=listen_for_server, args=(client,), daemon=True).start()

    while True:
        try:
            msg = input("")
            if msg.lower() == "quit":
                client.close()
                break
            client.send(msg.encode('utf-8'))
        except:
            break

if __name__ == "__main__":
    main()