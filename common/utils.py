import torch
import pickle

def serialize_weights(model):
    return {k: v.cpu() for k, v in model.state_dict().items()}

def deserialize_weights(model, weights):
    model.load_state_dict({k: v.to(next(model.parameters()).device) for k, v in weights.items()})
    return model
