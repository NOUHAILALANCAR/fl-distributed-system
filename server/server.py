import socket
import pickle
import threading
import time
from monitoring.logger import logger
from server.aggregator import FedAvgAggregator
from server.fault_tolerance import FaultTolerance
from server.checkpoint import save_checkpoint, load_latest_checkpoint
from common.utils import serialize_weights, deserialize_weights

class FederatedServer:
    def __init__(self, host='0.0.0.0', port=5000, max_rounds=10):
        self.host = host
        self.port = port
        self.max_rounds = max_rounds
        self.current_round = 0
        
        self.clients = {}           # client_id -> info
        self.updates = {}           # round -> list of updates
        self.aggregator = FedAvgAggregator()
        self.fault = FaultTolerance(quorum=3)
        
        self.lock = threading.Lock()

    def broadcast_model(self, round_num):
        """Envoie le modèle global à tous les clients"""
        weights = serialize_weights(self.aggregator.global_model)
        msg = {
            "type": "model",
            "round": round_num,
            "weights": weights
        }
        logger.info(f"📤 Broadcasting model for round {round_num} to {len(self.clients)} clients")
        
        # Pour simplifier : on envoie via une connexion séparée ou on garde la logique dans handle_client
        # Ici on suppose que les clients sont déjà connectés et en écoute

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(8192 * 4)
                if not data:
                    break
                    
                msg = pickle.loads(data)

                if msg["type"] == "register":
                    with self.lock:
                        self.clients[msg["client_id"]] = {
                            "addr": addr,
                            "data_size": msg["data_size"],
                            "last_seen": time.time()
                        }
                    logger.success(f"✅ Client registered: {msg['client_id']}")

                elif msg["type"] == "update":
                    with self.lock:
                        round_num = msg["round"]
                        if round_num not in self.updates:
                            self.updates[round_num] = []
                        
                        # Vérification byzantine
                        if self.fault.detect_byzantine(msg["weights"], serialize_weights(self.aggregator.global_model)):
                            logger.warning(f"❌ Client {msg['client_id']} rejected (Byzantine)")
                            continue
                            
                        self.updates[round_num].append(msg)
                        logger.info(f"📥 Update received from {msg['client_id']} (Round {round_num})")

        except Exception as e:
            logger.error(f"Client {addr} disconnected: {e}")
        finally:
            conn.close()

    def run_round(self):
        self.current_round += 1
        round_num = self.current_round
        logger.info(f"🔄 --- Starting Round {round_num}/{self.max_rounds} ---")

        self.updates[round_num] = []
        
        # Broadcast (simulé ici - dans une vraie version on peut ouvrir des connexions)
        self.broadcast_model(round_num)

        # Attendre les mises à jour (avec timeout)
        timeout = 25  # secondes
        start_time = time.time()
        while time.time() - start_time < timeout:
            with self.lock:
                if len(self.updates.get(round_num, [])) >= self.fault.quorum:
                    break
            time.sleep(2)

        # Agrégation
        with self.lock:
            updates = self.updates.get(round_num, [])
            active = [u["client_id"] for u in updates]
            
            if self.fault.check_quorum(updates):
                logger.info(f"⚖️ Aggregating {len(updates)} clients (Quorum OK)")
                self.aggregator.aggregate(updates)
                save_checkpoint(self.aggregator.global_model, round_num)
                logger.success(f"✅ Round {round_num} completed successfully!")
            else:
                logger.warning(f"⚠️ Quorum not reached ({len(updates)}/{self.fault.quorum})")

    def start(self):
        # Charger checkpoint
        checkpoint = load_latest_checkpoint()
        if checkpoint:
            self.current_round = checkpoint["round"]
            logger.info(f"🔄 Resumed from checkpoint round {self.current_round}")

        # Démarrage du serveur socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(10)
            logger.success(f"🚀 Federated Server started on {self.host}:{self.port}")

            # Thread pour accepter les connexions
            def accept_clients():
                while True:
                    conn, addr = server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

            threading.Thread(target=accept_clients, daemon=True).start()

            # Boucle principale des rounds
            while self.current_round < self.max_rounds:
                self.run_round()
                time.sleep(3)  # Pause entre rounds

            logger.success("🎉 Training finished successfully!")


if __name__ == "__main__":
    server = FederatedServer(max_rounds=10)
    server.start()
