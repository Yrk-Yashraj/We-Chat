# Importing necessary modules
import socket
import threading

# Server configuration
HOST = "127.0.0.1"
PORT = 5000
LISTENER_LIMIT = 5
active_clients = []  # Contains a list of all clients connected to this server

def send_messages_to_all(message):
    """Send a message to all connected clients."""
    for user in active_clients:
        send_message_to_client(user[1], message)


def send_message_to_client(client, message):
    """Send a message to a single client."""
    client.sendall(message.encode())


def listen_for_messages(client, username):
    """Listen for messages from a specific client and broadcast to others."""
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message != "":
                final = f"{username}~{message}"
                send_messages_to_all(final)
            else:
                print(f"The message sent from client {username} is empty.")
        except Exception as e:
            print(f"Error while listening for messages from {username}: {e}")
            break


def client_handler(client):
    """Handle a new client connection."""
    while True:
        try:
            username = client.recv(2048).decode("utf-8")
            if username != "":
                active_clients.append((username, client))
                break
            else:
                print("Client username is empty!")
        except Exception as e:
            print(f"Error while handling client connection: {e}")
            break

    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():
    # Creating the socket object for the server side
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try-except block
    try:
        server_socket.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind to Host {HOST} and Port {PORT}: {e}")
        return

    server_socket.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while True:
        client_socket, address = server_socket.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
