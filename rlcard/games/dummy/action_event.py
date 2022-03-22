from typing import List
from rlcard.games.base import Card
from .utils import  ID_2_ACTION, get_card, get_card_id, meld_2_rank

draw_card_action_id = 0
deposit_card_action_id = draw_card_action_id + 1
take_card_action_id = deposit_card_action_id + 329
meld_card_action_id  = take_card_action_id + 329
discard_action_id = meld_card_action_id + 329
knock_action_id = discard_action_id + 52

class ActionEvent:
    def __init__(self, action_id: int) -> None:
        self.action_id = action_id

    @staticmethod
    def get_num_actions():
        return 1093

    @staticmethod
    def decode_action(action_id) -> 'ActionEvent':
        if action_id == draw_card_action_id:
            action_event = DrawCardAction()
        elif action_id in range(deposit_card_action_id, take_card_action_id):
            action_event = DepositCardAction(action_id - deposit_card_action_id)
        elif action_id in range(take_card_action_id, meld_card_action_id):
            action_event = TakeCardAction(action_id - take_card_action_id)
        elif action_id in range(meld_card_action_id, discard_action_id):
            action_event = MeldCardAction(action_id - meld_card_action_id)
        elif action_id in range(discard_action_id, knock_action_id):
            card_id = action_id - discard_action_id
            card = get_card(card_id=card_id)
            action_event = DiscardAction(card=card)
        elif action_id in range(knock_action_id, knock_action_id + 53):
            card_id = action_id - knock_action_id
            action_event = KnockAction(None) if card_id == 52 else KnockAction(card=get_card(card_id=card_id))
        else:
            raise Exception("decode_action: unknown action_id={}".format(action_id))
        return action_event


class DrawCardAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=draw_card_action_id)

    def __str__(self):
        return "draw_card"

class DiscardAction(ActionEvent):
    def __init__(self, card: Card):
        card_id = get_card_id(card)
        super().__init__(action_id=discard_action_id + card_id)
        self.card = card

    def __str__(self):
        return "discard {}".format(self.card.get_index())

class TakeCardAction(ActionEvent):
    def __init__(self, rank_id: int):
        super().__init__(action_id = take_card_action_id + rank_id)
        self.rank_id = rank_id
    def __str__(self) -> str:
        return "takecard {}".format(ID_2_ACTION[self.rank_id])

class DepositCardAction(ActionEvent):

    def __init__(self, rank_id : int):
        super().__init__(action_id = deposit_card_action_id + rank_id)
        self.rank_id = rank_id

    def __str__(self) -> str:
        return "deposit {}".format(ID_2_ACTION[self.rank_id])

class MeldCardAction(ActionEvent):

    def __init__(self, rank_id :int):
        
        super().__init__(action_id = meld_card_action_id + rank_id)
        self.rank_id = rank_id

    def __str__(self):
        return "meldcard {}".format(ID_2_ACTION[self.rank_id])

class KnockAction(ActionEvent):

    def __init__(self, card: Card):
        card_id = 52 if card is None else get_card_id(card)
        super().__init__(action_id=knock_action_id + card_id)
        self.card = card

    def __str__(self):
        c = self.card.get_index() if self.card is not None else ""
        return "knock {}".format(c)