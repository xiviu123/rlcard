from math import e
from examples.human.dummy.game_board import GameBoard
from rlcard.games.dummy.action_event import ActionEvent
from rlcard.utils.utils import print_card
import numpy as np

class HumanAgent(object):
    ''' A human agent for Blackjack. It can be used to play alone for understand how the blackjack code runs
    '''

    def __init__(self, num_actions):
        ''' Initilize the human agent

        Args:
            num_actions (int): the size of the output action space
        '''
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''
        
        # _print_state(state['raw_obs'], state['raw_legal_actions'])
        print("[" + ", ".join(["{}-".format(a) + ActionEvent.decode_action(a).__str__() for a in state['raw_legal_actions']]) + "]")
        action_id = int(input('>> You choose action (integer): '))
        while action_id not in state['legal_actions']:
            print('Action illegel...')
            action_id = int(input('>> Re-choose action (integer): '))

        
        return ActionEvent.decode_action(action_id)

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
        '''
        return self.step(state), {}

def _print_state(state, raw_legal_actions):

    other_melds =                           state[-329:]
    current_melds =                         state[:-329][-329:]
    uknown_cards =                          state[:-329][:-329][-52:]
    top_discard =                           state[:-329][:-329][:-52][-52:]
    speto_cards =                           state[:-329][:-329][:-52][:-52][-52:]
    other_known_cards =                     state[:-329][:-329][:-52][:-52][:-52][-52:]
    opponent_ahead_known_cards =            state[:-329][:-329][:-52][:-52][:-52][:-52][-52:]
    discard =                               state[:-329][:-329][:-52][:-52][:-52][:-52][:-52][-52:]
    current_hand =                          state[:-329][:-329][:-52][:-52][:-52][:-52][:-52][:-52][-52:]
    num_stoke_pile =                        state[:-329][:-329][:-52][:-52][:-52][:-52][:-52][:-52][:-52][-29:]
    num_player =                            state[:-329][:-329][:-52][:-52][:-52][:-52][:-52][:-52][:-52][:-29][-4:]



    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the each player's historical actions
    '''
    


import rlcard
import torch
import os
ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')

env = rlcard.make('dummy')
device = torch.device('cpu')

model_path = os.path.join(ROOT_PATH, 'dummy_dmc', '{}.pth'.format(0))
agent = torch.load(model_path, map_location=device)
agent.set_device(device)

human_agent = HumanAgent(env.num_actions)

env.set_agents([human_agent, agent])


board = GameBoard()
env.game.add_action_call = board.bridge


while (True):
    print(">> Start a new game")
    trajectories, payoffs = env.run(is_training=False)

    print(trajectories, payoffs)

    input("Press any key to continue...")