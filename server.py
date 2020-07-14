import socket
import ast
from exchange import *
import pickle


def run_server():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, addr = server_socket.accept()
    print("server now running at: {0}".format(addr))

    market = Market()

    # now lets connect
    while True:
        # so the data that our client is going to pass to us is a string of a dict that is encoded
        payload = conn.recv(1024).decode()
        if not payload:
            # this stops the server when our client disconnects because we will no longer be getting any data
            break
        # so to break apart our data with the above invariant we do the following:
        # print(payload)
        try:
            data = ast.literal_eval(payload)  # this should return data as a dict
            # now let us create an exchange
            market.add_order_from_dict(data)
            # on order check send order list to client
            client_list = market.find_executions()
            # conn.send(str(client_list).encode())
            # trying out with pickle:
            conn.send(pickle.dumps(client_list))

        except Exception as e:
            print(e)
            conn.send("None")

    conn.close()


if __name__ == "__main__":
    run_server()
    # server_program()
