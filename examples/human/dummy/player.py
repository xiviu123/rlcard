from typing import List


class Player:
    def __init__(self, player_id: int) -> None:
        self.player_id = player_id
        self.hand = []
        self.melds = []
        self.known_cards = []