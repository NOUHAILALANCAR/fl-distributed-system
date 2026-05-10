import unittest
import time
from server.fault_tolerance import FaultTolerance

class TestFederatedLearning(unittest.TestCase):

    def test_quorum(self):
        ft = FaultTolerance(quorum=3)
        self.assertTrue(ft.check_quorum(["c1", "c2", "c3"]))
        self.assertFalse(ft.check_quorum(["c1", "c2"]))

    def test_byzantine_detection(self):
        ft = FaultTolerance()
        # Simulation simple
        fake_weights = {"layer1": 0}  # À adapter selon ta structure
        self.assertIsInstance(ft.detect_byzantine(fake_weights, fake_weights), bool)

    def test_backoff(self):
        ft = FaultTolerance()
        sleep_time = ft.exponential_backoff(3)
        self.assertLessEqual(sleep_time, 8)

if __name__ == "__main__":
    unittest.main()
