import socket
import pickle
import random
import time

from common.model import SimpleModel
from common.config import HOST, PORT
from client.local_training import train_local


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print("Connected to server")


while True:

    try:

        data = client_socket.recv(100000)

        if not data:
            break

        payload = pickle.loads(data)

        round_number = payload["round"]

        model_weights = payload["weights"]

        print(f"Round received : {round_number}")

        model = SimpleModel()

        model.load_state_dict(model_weights)

        updated_weights = train_local(model)

        if random.random() < 0.2:

            print("Packet lost")

            continue

        response = {

            "round": round_number,
            "weights": updated_weights
        }

        client_socket.send(pickle.dumps(response))

        print("Weights sent")

        time.sleep(2)

    except Exception as e:

        print("Error :", e)

        break


client_socket.close()
