import time
from monitoring.logger import logger

class FaultTolerance:
    def __init__(self, quorum=3):
        self.quorum = quorum
        self.heartbeats = {}
        self.max_l2_norm = 10.0  # Byzantine detection

    def check_quorum(self, active_clients):
        return len(active_clients) >= self.quorum

    def detect_byzantine(self, weights, reference_weights):
        # Simple L2 norm detection
        for key in weights:
            diff = torch.norm(weights[key] - reference_weights[key])
            if diff > self.max_l2_norm:
                return True
        return False

    def exponential_backoff(self, attempt):
        time.sleep(min(2 ** attempt, 8))
