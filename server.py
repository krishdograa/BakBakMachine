import socket
import threading
from cryptography.fernet import Fernet

# Generate an encryption key (store this securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Define server IP and port
HOST = '127.0.0.1'
PORT = 12345

clients = []  # List to hold connected clients

# Handle individual client connection
def handle_client(client_socket):
    while True:
        try:
            # Receive encrypted message from client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            
            # Broadcast the encrypted message to all other clients
            broadcast(encrypted_message, client_socket)
        
        except Exception as e:
            print(f"Error: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Broadcast message to all clients except the sender
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting: {e}")
                client.close()
                clients.remove(client)

# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    print(f"Encryption key (share this with clients): {key.decode()}")  # Share the key with clients
    
    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        
        # Start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
