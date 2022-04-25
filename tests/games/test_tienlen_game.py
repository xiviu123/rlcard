import unittest
import numpy as np
from rlcard.games.tienlen.action_event import ActionEvent, FourOfAKindAction, PairAction, Chain3Action, ThreeOfAKindAction, Chain2PairAction
from rlcard.games.tienlen.card import get_card, get_card_str, get_rank_id

from rlcard.games.tienlen.game import TienlenGame as Game
from rlcard.games.tienlen.judger import TienlenJudger
from rlcard.games.tienlen.utils import *

import itertools 

class TestTienlenGame(unittest.TestCase):

    def test_step(self):
        for i in range(1):
            game = Game()
            state, current_player_id = game.init_game()

            while not game.is_over():
                action = np.random.choice(list(state['actions']))
                # self.assertIn(action.action_id, get_action_ids)  # should be a get action
                state, next_player = game.step(action)

    def _1test_proceed_game(self):
        game = Game()
        state, current_player_id = game.init_game()
        next_player_id = (current_player_id + 1) % len(game.round.players)

        player = game.round.players[current_player_id]

        act = [get_card("3", "S"), get_card("4", "S"), get_card("5", "D"), get_card("6", "S")]
        hand = act + [get_card("6", "D")]
        player.hand = hand

        op_hand = [get_card("3", "C"), get_card("4", "C"), get_card("5", "H"), get_card("6", "C")]

        
        opponent = game.round.players[next_player_id]
        opponent.hand = op_hand
        
        game.judger.playable_cards[next_player_id] =  game.judger.playable_cards_from_hand(opponent.hand)

        action = ActionEvent.get_action("Chain4", act)
        state, next_player = game.step(action)


        self.assertEqual(next_player, next_player_id)
        print([action.cards for action in state['actions'] if action != "pass"])

    def test_cal_playable_cards(self):
        
        # game = Game()
        # state, current_player_id = game.init_game()
        # current_player = game.round.players[current_player_id]
        hand = [get_card("2", "S"), get_card("2", "C"), get_card("4", "S"), get_card("4", "C"), get_card("5", "S"), get_card("5", "D"), get_card("6", "S"), get_card("6", "C"), get_card("6", "H"), get_card("6", "D"), get_card("7", "S")]
        # print(TienlenJudger.playable_cards_from_hand(hand))
        # get_cards_from_action_id(1000)
        
    def _1test_get_gt_cards(self):
        game = Game()
        state, current_player_id = game.init_game()
        player = game.round.players[current_player_id]
        opponent = game.round.players[(current_player_id + 1) % 2]


        act = PairAction(19)
        opponent.actions_history.append(act)

        player.hand = [get_card("2", "S"), get_card("K", "C"), get_card("Q", "C"), get_card("J", "C"), get_card("J", "S"), get_card("6", "C"), get_card("6", "H")]
        game.judger.playable_cards[player.player_id] = game.judger.playable_cards_from_hand(player.hand)
        
        print(game.judger.get_gt_cards(player, opponent))

    def _1test_decode_action(self):
        action = PairAction(77)
        self.assertEqual(action.cards, [38, 51])

        action = ThreeOfAKindAction(51)
        self.assertEqual(action.cards, [25, 38, 51])

        action = FourOfAKindAction(12)
        self.assertEqual(action.cards, [12, 25, 38, 51])

        action = Chain3Action(639)
        self.assertEqual(action.cards, [48, 49, 50])

        action = Chain2PairAction(395)
        self.assertEqual(action.cards, [36, 49, 37, 50])

        action = ActionEvent.decode_action(0)
        self.assertEqual(action.__str__(), "pass")

        action = ActionEvent.decode_action(1)
        self.assertEqual(action.__str__(), "solo")
        action = ActionEvent.decode_action(52)
        self.assertEqual(action.__str__(), "solo")
        action = ActionEvent.decode_action(53)
        self.assertEqual(action.__str__(), "Pair")
        action = ActionEvent.decode_action(130)
        self.assertEqual(action.__str__(), "Pair")
        action = ActionEvent.decode_action(131)
        self.assertEqual(action.__str__(), "ThreeOfAKind")
        action = ActionEvent.decode_action(182)
        self.assertEqual(action.__str__(), "ThreeOfAKind")
        action = ActionEvent.decode_action(183)
        self.assertEqual(action.__str__(), "FourOfAKind")
        action = ActionEvent.decode_action(195)
        self.assertEqual(action.__str__(), "FourOfAKind")
        action = ActionEvent.decode_action(196)
        self.assertEqual(action.__str__(), "Chain2Pair")
        action = ActionEvent.decode_action(591)
        self.assertEqual(action.__str__(), "Chain2Pair")
        action = ActionEvent.decode_action(592)
        self.assertEqual(action.__str__(), "Chain3Pair")
        action = ActionEvent.decode_action(2751)
        self.assertEqual(action.__str__(), "Chain3Pair")
        action = ActionEvent.decode_action(2752)
        self.assertEqual(action.__str__(), "Chain4Pair")
        action = ActionEvent.decode_action(14415)
        self.assertEqual(action.__str__(), "Chain4Pair")
        action = ActionEvent.decode_action(14416)

        self.assertEqual(action.__str__(), "Chain3")
        action = ActionEvent.decode_action(15055)
        self.assertEqual(action.__str__(), "Chain3")

        action = ActionEvent.decode_action(15056)
        self.assertEqual(action.__str__(), "Chain4")
        action = ActionEvent.decode_action(17359)
        self.assertEqual(action.__str__(), "Chain4")

        action = ActionEvent.decode_action(17360)
        self.assertEqual(action.__str__(), "Chain5")
        action = ActionEvent.decode_action(25551)
        self.assertEqual(action.__str__(), "Chain5")

        action = ActionEvent.decode_action(25552)
        self.assertEqual(action.__str__(), "Chain6")
        action = ActionEvent.decode_action(54223)
        self.assertEqual(action.__str__(), "Chain6")

        action = ActionEvent.decode_action(54224)
        self.assertEqual(action.__str__(), "Chain7")
        action = ActionEvent.decode_action(152527)
        self.assertEqual(action.__str__(), "Chain7")

        action = ActionEvent.decode_action(152528)
        self.assertEqual(action.__str__(), "Chain8")
        action = ActionEvent.decode_action(480207)
        self.assertEqual(action.__str__(), "Chain8")

        action = ActionEvent.decode_action(480208)
        self.assertEqual(action.__str__(), "Chain9")
        action = ActionEvent.decode_action(1528783)
        self.assertEqual(action.__str__(), "Chain9")

        action = ActionEvent.decode_action(1528784)
        self.assertEqual(action.__str__(), "Chain10")
        action = ActionEvent.decode_action(4674511)
        self.assertEqual(action.__str__(), "Chain10")

        action = ActionEvent.decode_action(4674512)
        self.assertEqual(action.__str__(), "Chain11")
        action = ActionEvent.decode_action(13063119)
        self.assertEqual(action.__str__(), "Chain11")

        action = ActionEvent.decode_action(13063120)
        self.assertEqual(action.__str__(), "Chain12")
        action = ActionEvent.decode_action(29840335)
        self.assertEqual(action.__str__(), "Chain12")
        
    def test_get_action_from_card(self):
        action = ActionEvent.get_action("pass", None)
        self.assertEqual(action.__str__(), "pass")

        action = ActionEvent.get_action("solo", [get_card("3", "D")])
        self.assertEqual(get_card_str(ActionEvent.decode_action(action.action_id).cards[0]), "3D")

        action = ActionEvent.get_action("Pair", [get_card("3", "D"), get_card("3", "S")])
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, [0, 26])

        action = ActionEvent.get_action("ThreeOfAKind", [get_card("3", "C"), get_card("3", "S"), get_card("3", "H")])
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, [0, 13, 39])

        action = ActionEvent.get_action("FourOfAKind", [get_card("3", "C"), get_card("3", "S"), get_card("3", "H") , get_card("3", "D")])
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, [0, 13, 26, 39])

        cards = [get_card("4", "S"), get_card("4", "D"), get_card("5", "S") , get_card("5", "H")]
        action = ActionEvent.get_action("Chain2Pair", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("4", "S") , get_card("4", "C"), get_card("5", "S") , get_card("5", "C"), get_card("6", "S"), get_card("6", "C")]
        action = ActionEvent.get_action("Chain3Pair", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("4", "S") , get_card("4", "C"), get_card("5", "S") , get_card("5", "C"), get_card("6", "S"), get_card("6", "C"), get_card("7", "S"), get_card("7", "H")]
        action = ActionEvent.get_action("Chain4Pair", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S")]
        action = ActionEvent.get_action("Chain3", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S")]
        action = ActionEvent.get_action("Chain4", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S")]
        action = ActionEvent.get_action("Chain5", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C")]
        action = ActionEvent.get_action("Chain6", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D")]
        action = ActionEvent.get_action("Chain7", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D"), get_card("T", "D")]
        action = ActionEvent.get_action("Chain8", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D"), get_card("T", "D"), get_card("J", "D")]
        action = ActionEvent.get_action("Chain9", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D"), get_card("T", "D"), get_card("J", "D"), get_card("Q", "D")]
        action = ActionEvent.get_action("Chain10", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D"), get_card("T", "D"), get_card("J", "D"), get_card("Q", "D"), get_card("K", "D")]
        action = ActionEvent.get_action("Chain11", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)

        cards = [get_card("3", "D"),get_card("4", "S"), get_card("5", "S") , get_card("6", "S"), get_card("7", "S"), get_card("8", "C"), get_card("9", "D"), get_card("T", "D"), get_card("J", "D"), get_card("Q", "D"), get_card("K", "D"), get_card("A", "D")]
        action = ActionEvent.get_action("Chain12", cards)
        self.assertEqual(ActionEvent.decode_action(action.action_id).cards, cards)




if __name__ == '__main__':
    unittest.main()