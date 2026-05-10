import socket
import pickle
import threading
from monitoring.logger import logger
from server.aggregator import FedAvgAggregator
from server.fault_tolerance import FaultTolerance
from server.checkpoint import save_checkpoint, load_latest_checkpoint
from common.utils import serialize_weights

class FederatedServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.clients = {}
        self.aggregator = FedAvgAggregator()
        self.fault = FaultTolerance(quorum=3)
        self.current_round = 0
        self.max_rounds = 10

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(4096 * 8)
                if not data:
                    break
                msg = pickle.loads(data)

                if msg["type"] == "register":
                    self.clients[msg["client_id"]] = {"addr": addr, "data_size": msg["data_size"]}
                    logger.info(f"Client registered: {msg['client_id']}")

                elif msg["type"] == "update":
                    # Byzantine check + aggregation logic here
                    logger.info(f"Update received from {msg['client_id']} - Round {msg['round']}")

        except Exception as e:
            logger.error(f"Client error: {e}")

    def start(self):
        # Load checkpoint if exists
        checkpoint = load_latest_checkpoint()
        if checkpoint:
            self.current_round = checkpoint["round"]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            logger.info(f"Federated Server started on {self.host}:{self.port}")

            while self.current_round < self.max_rounds:
                self.current_round += 1
                logger.info(f"--- Starting Round {self.current_round} ---")

                # Broadcast model to clients (simplified)
                # In real version: send to all active clients

                # Wait for updates + aggregate
                time.sleep(8)  # simulation
                logger.success(f"Round {self.current_round} completed")

        logger.success("Training finished !")

if __name__ == "__main__":
    server = FederatedServer()
    server.start()
