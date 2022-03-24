from typing import List


class DummyPlayer:
    hand : List[int]
    melds: List[List[int]]
    known_cards : List[int]
    def __init__(self, player_id : int) -> None:
        self.hand = []
        self.player_id  = player_id
        self.melds = []
        self.known_cards = []

    def add_card_to_hand(self, card_id):
        self.hand.append(card_id)
    def remove_card_from_hand(self, card_id):
        self.hand.remove(card_id)