import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}  # Diccionario para almacenar información de clientes
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        print(f"Accepted connection from {address}")

        # Generar un identificador único para el cliente
        client_id = f"{address[0]}:{address[1]}"

        # Almacenar la información relevante del cliente
        self.clients[client_id] = {"host": address[0], "port": address[1]}

        # Imprimir la lista de clientes
        self.print_clients()

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received data from {address}: {data}")
            response = "Server received your message"
            client_socket.sendall(response.encode('utf-8'))

        # Eliminar la información del cliente que se desconecta
        del self.clients[client_id]

        # Imprimir la lista de clientes actualizada
        self.print_clients()

        client_socket.close()
        print(f"Connection with {address} closed")

    def print_clients(self):
        print("\nLista de clientes:")
        for client_id, client_info in self.clients.items():
            print(f"{client_id}: {client_info}")
        print("\n")

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    server = Server(HOST, PORT)
    server.start()
