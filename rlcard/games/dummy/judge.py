from typing import List


from typing import TYPE_CHECKING

from rlcard.games.dummy.player import DummyPlayer
from rlcard.games.dummy.utils.scorers import DummyScorer
if TYPE_CHECKING:
    from .game import DummyGame
from .utils.action_event import *
from .utils import melding as melding
import numpy as np

class DummyJudge:
    def __init__(self, game: 'DummyGame') -> None:
        self.game = game
        self.scorer = DummyScorer()

    def get_legal_actions(self) -> List[ActionEvent]:
        legal_actions = []  # type: List[ActionEvent]
        last_action = self.game.get_last_action()
        current_player = self.game.get_current_player()
        hand = current_player.hand

        if last_action is None or isinstance(last_action, DiscardAction):
            # Bốc bài DrawCardAction

            ## Bốc bài
            can_draw_card = len(self.game.round.dealer.stock_pile) > 0
            if can_draw_card:
                legal_actions.append(DrawCardAction())

        if last_action is None or isinstance(last_action, DiscardAction):
            # Ăn bài TakeCardAction

            temp_hand = hand + self.game.round.dealer.discard_pile
            clusters = melding.get_all_melds(temp_hand)
            
            for cluster in clusters:
                hand_card = [] 
                discard = []

                for card in cluster:
                    if card in hand:
                        hand_card.append(card)
                    else:
                        discard.append(card)
                
                if len(hand_card) < len(cluster) and len(hand_card) < len(hand):
                    legal_actions.append(TakeCardAction(hand_card+discard))
            
        if  isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, DepositCardAction) or \
            isinstance(last_action, MeldCardAction) or \
            isinstance(last_action, TakeCardAction): 
            # Dánh bài DiscardAction


            cards_to_discard = [card for card in hand]
            discard_actions = [DiscardAction(card=card) for card in cards_to_discard]
            legal_actions = legal_actions + discard_actions
            # print("check TakeCardAction: {}".format(len(hand)))

        if isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, TakeCardAction) or \
            isinstance(last_action, MeldCardAction) or \
            isinstance(last_action, DepositCardAction):
            #Hạ bài MeldCardAction

            if len(hand) <= 3:
                pass

            clusters = melding.get_all_melds(hand)
            
            for cluster in clusters:
                if len(cluster) < len(hand): 
                    legal_actions.append(MeldCardAction(cluster))

        if isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, TakeCardAction) or \
            isinstance(last_action, DepositCardAction) or \
            isinstance(last_action, MeldCardAction) :
            #Guiwr baif DepositCardAction
            if len(hand) <= 1:
                pass

            for card in hand:
                for meld in self.game.round.dealer.melds:
                    if melding.check_can_deposit(card, meld):
                        legal_actions.append(DepositCardAction(meld + [card]))

        if isinstance(last_action, MeldCardAction) or \
            isinstance(last_action, DepositCardAction) or \
            isinstance(last_action, TakeCardAction):

            # Ù KnockAction
            if len(hand) == 1:
                return [KnockAction(hand[0])]


        if isinstance(last_action, DiscardAction):
            if len(self.game.round.dealer.stock_pile) == 0:
                #game over
                return [KnockAction(None)]
            

        # print("uid: {uid}, last_action: {last_action}, hand: {hand}, discard_pile: {discard_pile}, stoke_pile: {stock}".format(uid=current_player.get_player_id(), last_action=last_action, hand= len(hand), discard_pile=len(self.game.round.dealer.discard_pile), stock=len(self.game.round.dealer.stock_pile)))
        # else:
        #     raise Exception('get_legal_actions: unknown last_action={}'.format(last_action))
        # print("list action: ", ",".join([action.__str__() for action in legal_actions]))
        return legal_actions
