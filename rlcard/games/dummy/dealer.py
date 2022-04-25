from typing import List
from .player import DummyPlayer as Player
import numpy as np
class DummyDealer:
    discard_pile : List[int]
    stock_pile : List[int]
    speto_cards: List[int]
    def __init__(self, np_random : np.random.RandomState) -> None:
        self.np_random = np_random
        self.discard_pile = []
        self.stock_pile = [i for i in range(52)]
        np_random.shuffle(self.stock_pile)
        self.speto_cards = [10, 13]

    def deal_cards(self, player: Player, num: int):
        ''' Deal some cards from stock_pile to one player

        Args:
            player (GinRummyPlayer): The GinRummyPlayer object
            num (int): The number of cards to be dealt
        '''
        for _ in range(num):
            player.hand.append(self.stock_pile.pop())

    def deal_first_card(self):
        self.first_card = self.stock_pile.pop()
        if self.first_card not in self.speto_cards:
            self.speto_cards.append(self.first_card)
        self.discard_pile.append(self.first_card)
        