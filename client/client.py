import torch
import socket
import pickle
import time
import random
from common.model import get_model
from common.utils import serialize_weights, deserialize_weights
from monitoring.logger import logger

class FederatedClient:
    def __init__(self, client_id, server_host='server', server_port=5000):
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        self.model = get_model()
        self.data_size = random.randint(800, 1200)

    def train_local(self, epochs=3):
        # Simulation d'entraînement (à remplacer par vrai dataloader si besoin)
        for _ in range(epochs):
            time.sleep(0.5)  # simulation
        logger.info(f"Client {self.client_id} finished local training")
        return serialize_weights(self.model)

    def start(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.server_host, self.server_port))
                    s.sendall(pickle.dumps({"type": "register", "client_id": self.client_id, "data_size": self.data_size}))

                    while True:
                        data = s.recv(4096 * 8)
                        if not data:
                            break
                        msg = pickle.loads(data)

                        if msg.get("type") == "model":
                            deserialize_weights(self.model, msg["weights"])
                            updated_weights = self.train_local()
                            
                            response = {
                                "type": "update",
                                "client_id": self.client_id,
                                "weights": updated_weights,
                                "data_size": self.data_size,
                                "round": msg["round"]
                            }
                            s.sendall(pickle.dumps(response))
            except Exception as e:
                logger.error(f"Connection lost: {e}")
                time.sleep(3)

if __name__ == "__main__":
    import os
    client = FederatedClient(os.getenv("CLIENT_ID", "client1"))
    client.start()
