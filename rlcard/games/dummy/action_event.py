from rlcard.games.base import Card
from .utils import  get_card, get_card_id

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
        if action_id in range(knock_action_id, knock_action_id + 53):
            card_id = action_id - knock_action_id
            action_event = KnockAction(None) if card_id == 52 else KnockAction(card=get_card(card_id=card_id))
        return action_event


class DiscardAction(ActionEvent):
    def __init__(self, card: Card):
        card_id = get_card_id(card)
        super().__init__(action_id=discard_action_id + card_id)
        self.card = card

    def __str__(self):
        return "discard {}".format(self.card.get_index())

class KnockAction(ActionEvent):

    def __init__(self, card: Card):
        card_id = 52 if card is None else get_card_id(card)
        super().__init__(action_id=knock_action_id + card_id)
        self.card = card

    def __str__(self):
        c = self.card.get_index() if self.card is not None else ""
        return "knock {}".format(c)