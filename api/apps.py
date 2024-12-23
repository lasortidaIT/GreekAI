import os
from django.apps import AppConfig
from django.conf import settings
import torch


class GreekAIModelConfig(AppConfig):
    name = 'api'
    MODEL_FILE = os.path.join(settings.MODELS, 'model_v2.pth')
    model = torch.load(MODEL_FILE, weights_only=False)
