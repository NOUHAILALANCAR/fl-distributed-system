import socket
import threading
import pickle

from common.model import SimpleModel
from common.config import *

from server.aggregation import fedavg
from server.checkpoint import save_checkpoint


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(NUM_CLIENTS)

print("Server started")


clients = []

model = SimpleModel()


def handle_client(conn, addr):

    print(f"Client connected : {addr}")

    clients.append(conn)


while len(clients) < NUM_CLIENTS:

    conn, addr = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()


for round_number in range(ROUNDS):

    print(f"ROUND {round_number}")

    payload = {

        "round": round_number,
        "weights": model.state_dict()
    }

    for client in clients:

        client.send(pickle.dumps(payload))

    client_updates = []

    for client in clients:

        try:

            client.settimeout(TIMEOUT)

            data = client.recv(100000)

            if data:

                response = pickle.loads(data)

                if response["round"] == round_number:

                    client_updates.append(
                        response["weights"]
                    )

        except:

            print("Client timeout")

    if len(client_updates) >= QUORUM:

        print("Quorum reached")

        new_weights = fedavg(client_updates)

        model.load_state_dict(new_weights)

        save_checkpoint(model, round_number)

        print("Global model updated")

    else:

        print("Quorum not reached")


print("Training finished")
