from rlcard.games.base import Card
from .player import DummyPlayer
from .utils import get_deck
import numpy as np


class DummyDealer:
    def __init__(self, np_random : np.random.RandomState) -> None:
        self.np_random = np_random
        self.speto_cards = []
        self.discard_pile = []  # type: List[Card]
        self.shuffled_deck = get_deck()
        self.np_random.shuffle(self.shuffled_deck)
        self.stock_pile = self.shuffled_deck.copy()  # type: List[Card]

    def deal_cards(self, player: DummyPlayer, num: int):
        ''' Deal some cards from stock_pile to one player
        Args:
            player (GinRummyPlayer): The GinRummyPlayer object
            num (int): The number of cards to be dealt
        '''
        for _ in range(num):
            card : Card = self.stock_pile.pop()
            if card.get_index() == "SQ" or card.get_index() == "C2":
                self.speto_cards.append(card)
            player.hand.append(card)
        # player.did_populate_hand()

    def deal_first_card(self):
        first_card = self.stock_pile.pop()
        if not first_card in self.speto_cards:
            self.speto_cards.append(first_card)
        self.discard_pile.append(first_card)