# Importing necessary modules
import socket
import threading

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def receive_server_messages(client_socket):
    while True:
        try:
            # Receive messages from the server
            message = client_socket.recv(2048).decode("utf-8")
            if message != "":
                username = message.split("~")[0]
                content = message.split("~")[1]
                print(f"[{username}] {content}")
            else:
                print("Empty message from the server!")
        except Exception as e:
            print(f"Error while receiving message from the server: {e}")
            break


def communicate_with_server(client_socket):
    # Get the username from the user
    username = input("Enter your username: ")
    if username != "":
        # Send the username to the server
        client_socket.sendall(username.encode())
    else:
        print("Username cannot be empty!")
        exit(0)

    # Start a thread to receive messages from the server
    threading.Thread(target=receive_server_messages, args=(client_socket,)).start()

    # Send messages to the server
    send_message_to_server(client_socket)


def send_message_to_server(client_socket):
    while True:
        try:
            # Get the message from the user
            message = input("Message: ")
            if message != "":
                # Send the message to the server
                client_socket.sendall(message.encode())
            else:
                print("Empty message!")
                exit(0)
        except Exception as e:
            print(f"Error while sending message to the server: {e}")
            break


def main():
    # Creating a socket object for the client side
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Successfully connected to the server!")
    except Exception as e:
        print(f"Unable to connect to the server {SERVER_HOST} {SERVER_PORT}: {e}")
        return

    # Communicate with the server
    communicate_with_server(client_socket)


if __name__ == "__main__":
    main()
