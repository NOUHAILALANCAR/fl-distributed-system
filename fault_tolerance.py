import time
import torch
from monitoring.logger import logger

class FaultTolerance:
    def __init__(self, quorum=3):
        self.quorum = quorum
        self.heartbeats = {}
        self.max_l2_norm = 15.0  # Seuil pour détection byzantine

    def check_quorum(self, active_clients):
        """Vérifie si on a assez de clients pour faire l'agrégation"""
        return len(active_clients) >= self.quorum

    def detect_byzantine(self, weights, reference_weights):
        """Détection simple des gradients byzantins via norme L2"""
        for key in weights:
            diff = torch.norm(weights[key] - reference_weights[key]).item()
            if diff > self.max_l2_norm:
                logger.warning(f"Gradient byzantin détecté ! Norme L2 = {diff:.2f}")
                return True
        return False

    def exponential_backoff(self, attempt: int):
        """Retry avec backoff exponentiel"""
        sleep_time = min(2 ** attempt, 8)
        time.sleep(sleep_time)
        return sleep_time
