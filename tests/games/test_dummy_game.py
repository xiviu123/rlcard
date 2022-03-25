import unittest
from rlcard.games.dummy.game import DummyGame as Game


import numpy as np

from rlcard.games.dummy.melding import get_card


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

    def test_deposit(self):
        game = Game()
        state, current_player_id = game.init_game()
        game.round.dealer.speto_cards = [10, 13, 20]
        current_player = game.round.players[current_player_id]
        current_player.hand = [5, 24, 43, 14, 39, 36, 33, 4, 3]
        current_player.melds = [[15, 16, 17]]
        game.round.dealer.discard_pile = [20, 29, 25, 41, 37, 48, 22, 19, 0, 27, 23]

        game.step(121)

    def _1test_proceed_game(self):
        game = Game()
        game.init_game()
        while not game.is_over():
            legal_actions = game.judge.get_legal_actions()
            action = np.random.choice(legal_actions)
            _, _ = game.step(action)


   


if __name__ == '__main__':
    unittest.main()