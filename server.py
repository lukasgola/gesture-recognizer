import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f'Starting server on {server_address[0]} port {server_address[1]}')

    while True:
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        try:
            print(f'Connection from {client_address}')
            
            while True:
                # Receive data from the client
                data = connection.recv(1024)  # Adjust buffer size if needed
                if not data:
                    break
                
                # Decode the received data
                message = data.decode('utf-8')
                print(f'Received: {message}')

        finally:
            connection.close()

if __name__ == "__main__":
    start_server()
