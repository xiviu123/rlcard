from typing import List

from rlcard.games.dummy.dummy_error import DummyProgramError
from .player import DummyPlayer
from .action_event import ActionEvent, DepositCardAction, DiscardAction, DrawCardAction, KnockAction, MeldCardAction, TakeCardAction
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

class DrawCardMove(PlayerMove):

    def __init__(self, player: DummyPlayer, action: DrawCardAction, card: Card):
        super().__init__(player, action)
        if not isinstance(action, DrawCardAction):
            raise DummyProgramError("action must be DrawCardAction.")
        self.card = card

    def __str__(self):
        return "{} {} {}".format(self.player, self.action, str(self.card))

class TakeCardMove(PlayerMove):
    def __init__(self, player: DummyPlayer, action: TakeCardAction):
        super().__init__(player, action)
        if not isinstance(action, TakeCardAction):
            raise DummyProgramError("action must be DiscardAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)
class DepositCardMove(PlayerMove):
    def __init__(self, player: DummyPlayer, action: DepositCardAction):
        super().__init__(player, action)
        if not isinstance(action, DepositCardAction):
            raise DummyProgramError("action must be DepositCardAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)

class MeldCardMove(PlayerMove):
    def __init__(self, player: DummyPlayer, action: MeldCardAction):
        super().__init__(player, action)
        if not isinstance(action, MeldCardAction):
            raise DummyProgramError("action must be MeldCardAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)

class DiscardMove(PlayerMove):
    def __init__(self, player: DummyPlayer, action: DiscardAction):
        super().__init__(player, action)
        if not isinstance(action, DiscardAction):
            raise DummyProgramError("action must be DiscardAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)

class KnockMove(PlayerMove):

    def __init__(self, player: DummyPlayer, action: KnockAction):
        super().__init__(player, action)
        if not isinstance(action, KnockAction):
            raise DummyProgramError("action must be KnockAction.")

    def __str__(self):
        return "{} {}".format(self.player, self.action)