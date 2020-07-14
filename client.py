import socket
from exchange import *
import ast
import pickle


def client():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    while True:
        message = input(" -> ")
        if message == "exit":
            break
        client_socket.send(message.encode())
        """
        So the issue we're running into with ast.literal_eval(payload) is that the payload is literally a string that looks like:
        `[(<exchange.Buy object at 0x11720cfd0>, <exchange.Sell object at 0x117217110>)]`
        The issue with that is the client has no idea what the exchange.Sell or buy object at a certain memory address is
        The solution is to either do all the handling on the server side and return a series of dictionaries
        OR we can return actual python objects using the pickle.dumps and pickle.loads functions
        """

        # so now we're trying this with pickle.loads:
        payload = pickle.loads(client_socket.recv(1024))
        print(payload)
        if len(payload) > 0:
            order_tuple = payload[0]
            print(order_tuple[0].price - order_tuple[1].price)

        # payload = client_socket.recv(1024).decode()
        # print(payload)
        #

    client_socket.close()


if __name__ == "__main__":
    client()
