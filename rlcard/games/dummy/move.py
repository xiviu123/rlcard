from typing import List

from rlcard.games.dummy.dummy_error import DummyProgramError
from .player import DummyPlayer
from .action_event import ActionEvent, KnockAction
from rlcard.games.base import Card
class DummyMove(object):
    pass

class PlayerMove(DummyMove):

    def __init__(self, player: DummyPlayer, action: ActionEvent):
        super().__init__()
        self.player = player
        self.action = action

class DealHandMove(DummyMove):

    def __init__(self, player_dealing: DummyPlayer, shuffled_deck: List[Card]):
        super().__init__()
        self.player_dealing = player_dealing
        self.shuffled_deck = shuffled_deck

    def __str__(self):
        shuffled_deck_text = " ".join([str(card) for card in self.shuffled_deck])
        return "{} deal shuffled_deck=[{}]".format(self.player_dealing, shuffled_deck_text)

class KnockMove(PlayerMove):

    def __init__(self, player: DummyPlayer, action: KnockAction):
        super().__init__(player, action)
        if not isinstance(action, KnockAction):
            raise DummyProgramError("action must be KnockAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)