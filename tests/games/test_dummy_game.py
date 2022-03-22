import unittest
from rlcard.games.dummy.game import DummyGame as Game


import numpy as np
from rlcard.games.dummy.action_event import ActionEvent, TakeCardAction

from rlcard.games.base import Card
from rlcard.games.dummy.melding import *

class TestDummyGame(unittest.TestCase):
    def test_get_num_players(self):
        game = Game()
        num_players = game.get_num_players()
        self.assertEqual(num_players, 2)
    def test_get_num_actions(self):
        game = Game()
        num_actions = game.get_num_actions()
        self.assertEqual(num_actions, 1093)

    def test_init_game(self):
        game = Game()
        state, current_player = game.init_game()
        opponent_player = (current_player + 1) % 2
        self.assertEqual(len(game.round.move_sheet), 1)
        self.assertIn(current_player, [0, 1])
        self.assertIn(game.round.dealer_id, [0, 1])
        self.assertEqual(len(game.actions), 0)
        self.assertEqual(opponent_player, game.round.dealer_id)  # opponent_player is dealer
        self.assertEqual(len(game.round.players[opponent_player].hand), 11)  # dealer has 10 cards
        self.assertEqual(len(game.round.players[current_player].hand), 11)  # current_player has 11 cards
        self.assertEqual(len(game.round.dealer.shuffled_deck), 52)
        self.assertEqual(len(game.round.dealer.stock_pile), 29)
        self.assertEqual(len(game.round.dealer.discard_pile), 1)
        self.assertEqual(state['player_id'], current_player)
        self.assertEqual(len(state['hand']), 11)


    def _1test_meld_card(self):
        game= Game()
        _, current_player = game.init_game()
        player = game.get_current_player()
        card1 = Card("S", "2")
        card2 =  Card("S", "3")
        card3 = Card("S", "4")
        card4 = Card("S", "5")

        player.hand = [card3, card1, card2, card4]
        game.round.dealer.discard_pile = []
        game.round.dealer.stock_pile = []

        game.step(MeldCardAction([card3, card2, card1]))

    def _1test_meld_card(self):
        hand = [Card("H", "A"),Card("H", "2"), Card("H", "3")]
        discard = [ Card("H", "4")]

        clusters = get_all_melds(hand + discard)
            
        for cluster in clusters:
            
            print("==".join([c.rank + c.suit for c in cluster]))
    def _1test_take_card(self):
        game = Game()

        _, current_player = game.init_game()
        player = game.get_current_player()

        
        card1 = Card("S", "2")
        card2 =  Card("S", "3")
        card3 = Card("S", "4")
        card4 = Card("S", "5")

        player.hand = [card3, card4]

        game.round.dealer.discard_pile = [card1, card2]
        game.round.dealer.stock_pile = []
        
        game.step(TakeCardAction([card3, card2, card1, card4]))

        # print("know_card= {know_card}".format(know_card = len(player.known_cards)))

    def test_get_legal(self):
        game = Game()
        _, current_player = game.init_game()
        game.round.dealer.discard_pile =  [Card("H", "K"),  Card("S", "7"), Card("H", "T"),  Card("D", "8")]
        game.round.dealer.stock_pile  = [Card("H", "J")]
        player = game.get_current_player()
        player.hand = [Card("D", "5"), Card("S", "4"),Card("D", "Q"),Card("C", "K"),Card("D", "2"),Card("H", "6"),Card("H", "A"),Card("S", "K")]
        print(", ".join(a.__str__() for a in game.judge.get_legal_actions()))

    def _1test_step(self):
        game = Game()
        _, current_player = game.init_game()
        # opponent_player = (current_player + 1) % 2
        # action = np.random.choice(game.judge.get_legal_actions())
        # # self.assertIn(action.action_id, put_action_ids)  # should be a put action
        # _, next_player = game.step(action)
        
        while not game.is_over():
            player = game.get_current_player()
            legal_actions = game.judge.get_legal_actions()
            action = np.random.choice(legal_actions)
            # self.assertIn(action.action_id, get_action_ids)  # should be a get action
            _, next_player = game.step(action)
            

            print("uid: {uid}, action: {action}, hand: {hand}, discard_pile: {discard_pile}, stoke_pile: {stock}, know_card= {know_card}".format(uid=current_player, action=game.get_last_action(), hand= len(player.hand), discard_pile=len(game.round.dealer.discard_pile), stock=len(game.round.dealer.stock_pile), know_card = len(player.known_cards)))
            # current_player = next_player
            # self.assertEqual(next_player, opponent_player)  # keep turn to put card




if __name__ == '__main__':
    unittest.main()