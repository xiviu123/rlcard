from rlcard.games.base import Card


class DummyPlayer:
    def __init__(self, player_id: int, np_random) -> None:
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.known_cards = []
        self.melds = []
        self.transactions = []

    def add_card_to_hand(self, card: Card):
        self.hand.append(card)

    def remove_card_from_hand(self, card: Card):
        self.hand.remove(card)

    def add_transation(self, score : int):
        self.transactions.append(score)