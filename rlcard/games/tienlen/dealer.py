from typing import List
import numpy as np

from rlcard.games.tienlen.utils import init_standard_deck

from .player import TienlenPlayer as Player
class TienlenDealer:
    def __init__(self, np_random: np.random.RandomState) -> None:
        self.np_random = np_random
        self.deck = init_standard_deck()

    def shuffle(self):
        ''' Randomly shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players: List[Player]):
        ''' Deal cards to players

        Args:
            players (list): list of DoudizhuPlayer objects
        '''
        self.shuffle()
        hand_num = 13
        for  player in players:
            for _ in range(hand_num):
                card = self.deck.pop()
                player.hand.append(card)
            