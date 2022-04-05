from collections import OrderedDict
import os
import unittest

import torch
import rlcard
from rlcard.games.dummy.action_event import get_action_str
from rlcard.games.dummy.game import DummyGame as Game

from heapq import nlargest

import numpy as np

from rlcard.games.dummy.melding import *
from rlcard.games.dummy.utils import ID_2_ACTION, encode_cards, get_one_hot_array

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
        game.round.dealer.speto_cards = [10, 13, 6]
        game.round.dealer.discard_pile = [49]
        current_player = game.round.players[current_player_id]
        opponent = game.round.players[(current_player_id + 1) % 2]
        opponent.hand = [ 4, 27, 15, 0, 46, 42, 20, 9]

        current_player.hand =[51, 40, 37, 36, 34, 7, 23, 30, 8, 35, 10]
        current_player.melds = []
        opponent.melds = [[6, 32, 45]]

        state = game.get_state(current_player_id)
        state['actions'] = game.judge.get_legal_actions()
        state = self._extract_state(state)
        
        ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')
        device = torch.device('cpu')



        model_path = os.path.join(ROOT_PATH, 'dummy_dmc', '{}.pth'.format(1))
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
        action, info = agent.eval_step(state)
       

        actions = nlargest(3, info['values'], key=info['values'].get)
        print(info)
        # game.step(604)
        # print(game.judge.get_legal_actions())

    def _extract_state(self, state):
        num_stoke_pile  = state['num_stoke_pile']
        opponent_card_left = state['opponent_card_left']
        current_hand = state['current_hand']
        current_card_left = state['current_card_left']
        current_score_cards = state['current_score_cards']
        opponent_score_cards = state['opponent_score_cards']
        known_cards = state['known_cards']
        unknown_cards = state['unknown_cards']
        speto_card = state['speto_card']
        just_discard = state['just_discard']
        depositable_cards = state['depositable_cards']
        discard_pile =  state['discard_pile']

        num_stoke_pile_rep = get_one_hot_array(num_stoke_pile,29)
        opponent_card_left_rep = get_one_hot_array(opponent_card_left, 40)
        current_hand_rep = encode_cards(current_hand)
        current_card_left_rep = get_one_hot_array(current_card_left, 40)
        known_cards_rep = encode_cards(known_cards)
        unknown_cards_rep = encode_cards(unknown_cards)
        speto_card_rep = get_one_hot_array(speto_card,52)
        just_discard_rep = encode_cards(just_discard)
        depositable_cards_rep = encode_cards(depositable_cards)
        discard_pile_rep = encode_cards(discard_pile)
        current_score_cards_rep = encode_cards(current_score_cards)
        opponent_score_cards_rep = encode_cards(opponent_score_cards)

        obs = np.concatenate((
            num_stoke_pile_rep,
            opponent_card_left_rep,
            current_hand_rep,
            current_card_left_rep,
            known_cards_rep,
            unknown_cards_rep,
            speto_card_rep,
            just_discard_rep,
            depositable_cards_rep,
            discard_pile_rep,
            current_score_cards_rep,
            opponent_score_cards_rep
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