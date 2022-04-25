from typing import List
from typing import TYPE_CHECKING

from rlcard.games.tienlen.action_event import ActionEvent

if TYPE_CHECKING:
    from .judger import TienlenJudger as Judger
    from .player import TienlenPlayer as Player
import numpy as np


class TienlenPlayer:
    hand : List[int]
    actions_history: list
    played_cards: list
    def __init__(self, player_id: int, np_random: np.random.RandomState) -> None:
        self.player_id = player_id
        self.np_random = np_random
        self.hand = []
        self.actions_history = []
        
        

    def available_actions(self, greater_player,  judger : 'Judger'=None):
        actions = []
        if greater_player is None or greater_player.player_id == self.player_id:
            actions = judger.get_playable_cards(self)
        else:
            actions = judger.get_gt_cards(self, greater_player)

        return actions

    def play(self, action, greater_player=None):
        
        self.actions_history.append(action)
        if action == 'pass':
            return greater_player
        else:
            self.played_cards = action.cards
            self.removeCard(self.played_cards)
            
        
            #TODO
            return self

    def removeCard(self, cards):
        if not set(cards).issubset(self.hand):
            raise Exception("remove card error")
        self.hand = [card for card in self.hand if card not in cards]

    def get_last_action(self):
        return self.actions_history[-1]