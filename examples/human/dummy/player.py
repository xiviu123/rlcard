from typing import List


class Player:
    def __init__(self, player_id: int, hand: List[int] = [], meld: List[List[int]] = []) -> None:
        self.player_id = player_id
        self.hand = hand
        self.melds = meld