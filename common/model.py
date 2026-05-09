import torch
import torch.nn as nn


class SimpleModel(nn.Module):

    def __init__(self):
        super(SimpleModel, self).__init__()

        self.fc1 = nn.Linear(10, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):

        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x
