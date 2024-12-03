import os
from django.apps import AppConfig
from django.conf import settings
import torch
from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.con = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(16, 16, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 64, kernel_size=3),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(21632, 32),
            nn.ReLU(),
            nn.Linear(32, 48)
        )
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.con(x)
        x = x.view(-1, 21632)
        logits = self.linear_relu_stack(x)
        output = self.softmax(logits)
        return output

class GreekAIModelConfig(AppConfig):
    name = 'api'
    MODEL_FILE = os.path.join(settings.MODELS, 'weights.pt')
    model = NeuralNetwork()
    model.load_state_dict(torch.load(MODEL_FILE, weights_only=True, map_location=torch.device('cpu')))
