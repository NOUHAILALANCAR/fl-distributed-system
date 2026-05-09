import torch


def train_local(model):

    for param in model.parameters():

        param.data += torch.randn_like(param) * 0.01

    return model.state_dict()
