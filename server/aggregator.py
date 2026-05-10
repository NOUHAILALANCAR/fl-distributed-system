import torch
from common.utils import deserialize_weights
from common.model import get_model

class FedAvgAggregator:
    def __init__(self):
        self.global_model = get_model()

    def aggregate(self, client_updates):
        total_size = sum(update["data_size"] for update in client_updates)
        averaged_weights = {}

        for key in self.global_model.state_dict().keys():
            weighted_sum = torch.zeros_like(self.global_model.state_dict()[key])
            for update in client_updates:
                weighted = update["weights"][key] * (update["data_size"] / total_size)
                weighted_sum += weighted
            averaged_weights[key] = weighted_sum

        self.global_model.load_state_dict(averaged_weights)
        return serialize_weights(self.global_model)  # from utils
