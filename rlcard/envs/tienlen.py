from collections import OrderedDict
from rlcard.envs import Env
import numpy as np
from rlcard.games.tienlen.game import TienlenGame as Game
from rlcard.games.tienlen.utils import encode_cards, encode_players_round_active, get_one_hot_array

class TienlenEnv(Env):
    def __init__(self, config):
        self.name = 'tienlen'
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[100] for _ in range(self.num_players)]
        self.action_shape = [[54] for _ in range(self.num_players)]

    def _extract_state(self, state):
        '''
            current_hand
            current_played_cards
            players_round_active
            unknown_cards

            up_opponent_played_cards
            up_opponent_num_cards_left
            down_opponent_played_cards
            down_opponent_num_cards_left
            op_opponent_played_cards
            op_opponent_num_cards_left
        '''

        player_id =  state['player_id']
        current_hand = encode_cards(state['current_hand'])
        players_round_active = encode_players_round_active(state['players_round_active'])
        unknown_cards = encode_cards(state['unknown_cards'])

        num_cards_left = state['num_cards_left']
        played_cards = state['played_cards']

        current_played_cards = encode_cards(played_cards[player_id])
        
        up_opponent_id = ( player_id + 1) % self.game.num_players
        up_opponent_played_cards = encode_cards(played_cards[up_opponent_id])
        up_opponent_num_cards_left = get_one_hot_array(num_cards_left[up_opponent_id], 13)

        if self.game.num_players >= 2:
            down_opponent_id = self.game.num_players - player_id - 1
            down_opponent_played_cards = encode_cards(played_cards[down_opponent_id])
            down_opponent_num_cards_left = get_one_hot_array(num_cards_left[down_opponent_id], 13)

        if self.game.num_players == 4:
            op_opponent_id = ( player_id + 2) % self.game.num_players
            op_opponent_played_cards = encode_cards(played_cards[op_opponent_id])
            op_opponent_num_cards_left = get_one_hot_array(num_cards_left[op_opponent_id], 13)
        

        if self.game.num_players == 2:
            obs = np.concatenate((current_hand,
            current_played_cards,
            players_round_active,
            unknown_cards,

            up_opponent_played_cards,
            up_opponent_num_cards_left))
        elif self.game.num_players == 3:
            obs = np.concatenate((current_hand,
            current_played_cards,
            players_round_active,
            unknown_cards,

            up_opponent_played_cards,
            up_opponent_num_cards_left,
            down_opponent_played_cards,
            down_opponent_num_cards_left))
        
        elif self.game.num_players == 4:
            obs = np.concatenate((current_hand,
            current_played_cards,
            players_round_active,
            unknown_cards,

            up_opponent_played_cards,
            up_opponent_num_cards_left,
            down_opponent_played_cards,
            down_opponent_num_cards_left,
            op_opponent_played_cards,
            op_opponent_num_cards_left))
        
        legal_actions = OrderedDict({action_id: None for action_id in state['actions']})

        extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = list(legal_actions.keys())
        return extracted_state

    def _decode_action(self, action):
        return action

    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        return self.game.judger.get_payoffs()
