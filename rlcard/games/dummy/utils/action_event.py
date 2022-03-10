from typing import List
from rlcard.games.dummy.utils.card import Card
from . import utils as utils

'''
1093

draw_card_action_id = 0  = 0
deposit_card_action_id = 1  1   <=  A < 330
take_card_action_id = 330   330 <=  A < 659
meld_card_action_id = 659   659 <=  A < 988
discard_action_id =   988   988 <=  A < 1040
knock_action_id =   1040    1040 <=  A < 1093
'''
draw_card_action_id = 0
deposit_card_action_id = draw_card_action_id + 1
take_card_action_id = deposit_card_action_id + 329
meld_card_action_id  = take_card_action_id + 329
discard_action_id = meld_card_action_id + 329
knock_action_id = discard_action_id + 52

class ActionEvent(object):
    def __init__(self, action_id: int):
        self.action_id = action_id

    @staticmethod
    def get_num_actions():
        ''' Return the number of possible actions in the game
        '''
        return knock_action_id + 53  # 53 is case finish game without knock

    @staticmethod
    def decode_action(action_id) -> 'ActionEvent':
        ''' Action id -> the action_event in the game.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        '''

        # print(draw_card_action_id, deposit_card_action_id, take_card_action_id, meld_card_action_id, discard_action_id, knock_action_id)

        if action_id == draw_card_action_id:
            action_event = DrawCardAction()
        elif action_id in range(deposit_card_action_id, take_card_action_id):
            ranks = utils.ID_2_ACTION[action_id - deposit_card_action_id]
            action_event = DepositCardAction(utils.rank_2_meld(ranks))
        elif action_id in range(take_card_action_id, meld_card_action_id):
            ranks = utils.ID_2_ACTION[action_id - take_card_action_id]
            action_event = TakeCardAction(utils.rank_2_meld(ranks))
        elif action_id in range(meld_card_action_id, discard_action_id):
            ranks = utils.ID_2_ACTION[action_id - meld_card_action_id]
            action_event = MeldCardAction(utils.rank_2_meld(ranks))
        elif action_id in range(discard_action_id, knock_action_id):
            card_id = action_id - discard_action_id
            card = utils.get_card(card_id=card_id)
            action_event = DiscardAction(card=card)
        elif action_id in range(knock_action_id, knock_action_id + 53):
            card_id = action_id - knock_action_id
            if card_id == 52:
                action_event = KnockAction(None)
            else:
                card = utils.get_card(card_id=card_id)
                action_event = KnockAction(card=card)
        else:
            print(knock_action_id)
            raise Exception("decode_action: unknown action_id={}".format(action_id))

        return action_event

class DrawCardAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=draw_card_action_id)

    def __str__(self):
        return "draw_card"

class TakeCardAction(ActionEvent):
    def __init__(self, cards: List[Card]):
        action_id = utils.meld_2_rank(cards)
        super().__init__(action_id = take_card_action_id + action_id)
        self.cards = cards
    def __str__(self) -> str:
        return "takecard {}".format(utils.ID_2_ACTION[utils.meld_2_rank(self.cards)])

class DepositCardAction(ActionEvent):

    def __init__(self, cards : List[Card]):
        action_id = utils.meld_2_rank(cards)
        super().__init__(action_id = deposit_card_action_id + action_id)
        self.cards = cards

    def __str__(self) -> str:
        return "deposit {}".format(utils.ID_2_ACTION[utils.meld_2_rank(self.cards)])

class MeldCardAction(ActionEvent):

    def __init__(self, cards : List[Card]):
        
        action_id = utils.meld_2_rank(cards)
        super().__init__(action_id = meld_card_action_id + action_id)
        self.cards = cards

    def __str__(self):
        return "meldcard {}".format(utils.ID_2_ACTION[utils.meld_2_rank(self.cards)])


class DiscardAction(ActionEvent):

    def __init__(self, card: Card):
        card_id = utils.get_card_id(card)
        super().__init__(action_id=discard_action_id + card_id)
        self.card = card

    def __str__(self):
        return "discard {}".format(self.card.get_index())


class KnockAction(ActionEvent):

    def __init__(self, card: Card):
        if card is not None:
            card_id = utils.get_card_id(card)
        else:
            card_id = 52
        super().__init__(action_id=knock_action_id + card_id)
        self.card = card

    def __str__(self):
        c = self.card.get_index() if self.card is not None else ""
        return "knock {}".format(c)