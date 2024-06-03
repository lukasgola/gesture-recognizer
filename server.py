import socket
import struct

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
                # First, receive the size of the incoming data
                data_size = connection.recv(4)
                if not data_size:
                    break
                
                # Unpack the size of the data
                data_size = struct.unpack('!I', data_size)[0]

                # Now receive the actual data
                data = b''
                while len(data) < data_size:
                    packet = connection.recv(data_size - len(data))
                    if not packet:
                        break
                    data += packet
                
                if data:
                    print(f'Received: {data}')
                else:
                    break

        finally:
            connection.close()

if __name__ == "__main__":
    start_server()
