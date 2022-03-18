import os

import torch

import rlcard

from rlcard.models.model import Model

# Root path of pretrianed models
ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')

class DummyDMCModel(Model):
    def __init__(self):
        ''' Load pretrained model
        '''
        self.agents = []
        device = torch.device('cpu')

        for i in range(2):
            model_path = os.path.join(ROOT_PATH, 'dummy_dmc', '{}.pth'.format(i))
            agent = torch.load(model_path, map_location=device)
            agent.set_device(device)

            self.agents.append(agent)


