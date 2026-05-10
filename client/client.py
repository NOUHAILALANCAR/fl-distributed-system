import socket
import pickle
import time
import random
import os
from common.model import get_model
from common.utils import serialize_weights, deserialize_weights
from monitoring.logger import logger

class FederatedClient:
    def __init__(self, client_id=None, server_host='server', server_port=5000):
        self.client_id = client_id or f"client-{random.randint(1000,9999)}"
        self.server_host = server_host
        self.server_port = server_port
        self.model = get_model()
        self.data_size = random.randint(600, 1500)

    def train_local(self, epochs=3):
        logger.info(f"🏋️ Client {self.client_id} starting local training ({epochs} epochs)")
        # Simulation d'entraînement
        for epoch in range(epochs):
            time.sleep(0.8)
            logger.debug(f"Client {self.client_id} - epoch {epoch+1}/{epochs}")
        return serialize_weights(self.model)

    def start(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.server_host, self.server_port))
                    
                    # Enregistrement
                    s.sendall(pickle.dumps({
                        "type": "register",
                        "client_id": self.client_id,
                        "data_size": self.data_size
                    }))

                    while True:
                        data = s.recv(8192 * 4)
                        if not data:
                            break
                            
                        msg = pickle.loads(data)
                        
                        if msg.get("type") == "model":
                            deserialize_weights(self.model, msg["weights"])
                            logger.info(f"📥 Received global model - Round {msg['round']}")

                            updated_weights = self.train_local(epochs=3)

                            response = {
                                "type": "update",
                                "client_id": self.client_id,
                                "weights": updated_weights,
                                "data_size": self.data_size,
                                "round": msg["round"]
                            }
                            s.sendall(pickle.dumps(response))
                            logger.success(f"📤 Sent update to server - Round {msg['round']}")

            except Exception as e:
                logger.error(f"Connection lost, retrying... ({e})")
                time.sleep(3)


if __name__ == "__main__":
    client = FederatedClient(client_id=os.getenv("CLIENT_ID"))
    client.start()
