from collections import OrderedDict
import os
import unittest

import torch
import rlcard
from rlcard.games.dummy.action_event import get_action, get_action_str
from rlcard.games.dummy.game import DummyGame as Game

from heapq import nlargest

import numpy as np

from rlcard.games.dummy.melding import *
from rlcard.games.dummy.utils import ID_2_ACTION, encode_cards, encode_melds, get_one_hot_array

class TestDummyGame(unittest.TestCase):
    def test_get_num_players(self):
        game = Game()
        num_players = game.num_players
        self.assertEqual(num_players, 2)
    def test_get_num_actions(self):
        game = Game()
        num_actions = game.get_num_actions()
        self.assertEqual(num_actions, 1093)

    def _1test_init_game(self):
        game = Game()
        state, current_player = game.init_game()
        opponent_player = (current_player + 1) % 2
        self.assertEqual(len(game.round.players[opponent_player].hand), 11)  # dealer has 10 cards
        self.assertEqual(len(game.round.players[current_player].hand), 11)  # current_player has 11 cards
        self.assertEqual(len(game.round.dealer.stock_pile), 29)
        self.assertEqual(len(game.round.dealer.discard_pile), 1)
        self.assertEqual(state['player_id'], current_player)

    def _1test_deposit(self):
        game = Game()
        state, current_player_id = game.init_game()
        game.round.dealer.speto_cards = [10, 13, 20]
        current_player = game.round.players[current_player_id]
        current_player.hand = [5, 24, 43, 14, 39, 36, 33, 4, 3]
        current_player.melds = [[15, 16, 17]]
        game.round.dealer.discard_pile = [20, 29, 25, 41, 37, 48, 22, 19, 0, 27, 23]

        game.step(121)

    def test_model(self):
        game = Game()
        state, current_player_id = game.init_game()
        game.round.dealer.stock_pile = game.round.dealer.stock_pile[:22]
        game.round.dealer.speto_cards = [10, 13, 17]
        game.round.dealer.discard_pile = [39]
        current_player = game.round.players[current_player_id]
        opponent = game.round.players[(current_player_id + 1) % 2]
        opponent.known_cards = [6]

        current_player.hand =[8,36,26,43,38,0,51,30]
        current_player.melds = [[16,18,17],[35,33,34]]
        opponent.melds = [[4,3,5]]

        state = game.get_state(current_player_id)
        game.actions.append(0)
        state['actions'] = game.judge.get_legal_actions()
        state = self._extract_state(state)
        
        ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')
        device = torch.device('cpu')



        model_path = os.path.join(ROOT_PATH, 'dummy_dmc', 'two_players', '{}.pth'.format(1))
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
        action, info = agent.eval_step(state)
       

        actions = nlargest(30, info['values'], key=info['values'].get)
        print(actions)

        for a in actions:
            print(get_action(a))
        # game.step(604)
        # print(game.judge.get_legal_actions())

    def _extract_state(self, state):
        num_stoke_pile  = state['num_stoke_pile']
        up_opponent_card_left = state['up_opponent_card_left']
        up_opponent_meld = state['up_opponent_meld']
        up_opponent_hand = state['up_opponent_hand']
        current_hand = state['current_hand']
        current_meld = state['current_meld']
        discard_pile = state['discard_pile']
        known_cards = state['known_cards']
        speto_card = state['speto_card']

        print(num_stoke_pile)
        print(up_opponent_card_left)
        print(up_opponent_meld)
        print(up_opponent_hand)
        print(current_hand)
        print(current_meld)
        print(discard_pile)
        print(known_cards)
        print(speto_card)

        num_stoke_pile_rep = get_one_hot_array(num_stoke_pile,29)
        up_opponent_card_left_rep = get_one_hot_array(up_opponent_card_left, 40)
        up_opponent_meld_rep = encode_melds( up_opponent_meld)
        up_opponent_hand_rep = encode_cards(up_opponent_hand)
        current_hand_rep = encode_cards(current_hand)
        current_meld_rep = encode_melds(current_meld)
        discard_pile_rep = encode_cards(discard_pile)
        known_cards_rep = encode_cards(known_cards)
        speto_card_rep = encode_cards(speto_card)


        

        obs = np.concatenate((
            num_stoke_pile_rep,
            up_opponent_card_left_rep,
            up_opponent_meld_rep,
            up_opponent_hand_rep,
            current_hand_rep,
            current_meld_rep,
            discard_pile_rep,
            known_cards_rep,
            speto_card_rep
        ))


        legal_actions =  {action_id: None for action_id in state['actions']}

        extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = list(legal_actions.keys())

        # extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
        # extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['actions']]
        return extracted_state

        
    def _1test_proceed_game(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            legal_actions = game.judge.get_legal_actions()
            action = np.random.choice(legal_actions)
            _, _ = game.step(action)

    def _1test_legal_action(self):
        game = Game()
        state, current_player_id = game.init_game()
        current_player = game.round.players[current_player_id]
        current_player.hand = [4]

        game.round.dealer.discard_pile = [5, 1,2]



        legal_actions = game.judge.get_legal_actions()

        print(legal_actions)



if __name__ == '__main__':
    unittest.main()