from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import DummyGame

from rlcard.games.dummy.action_event import ACTION, get_action_str
from rlcard.games.dummy.utils import ID_2_ACTION
from .melding import *
from rlcard.games.dummy.action_event import draw_card_action_id, take_card_action_id, discard_action_id, deposit_card_action_id, meld_card_action_id, knock_action_id
class DummyJudge:
    def __init__(self, game: 'DummyGame') -> None:
        self.game = game

    def  get_legal_actions(self):
        legal_actions  = []
        last_action = self.game.get_last_action()
        current_player = self.game.round.players[self.game.round.current_player_id]
        current_hand = current_player.hand
        all_melds = [meld for p in self.game.round.players for meld in p.melds]
        current_melds = self.game.round.players[self.game.round.current_player_id].melds
        num_stoke_pile = len(self.game.round.dealer.stock_pile)
        discard_pile = self.game.round.dealer.discard_pile
        
        if last_action is None or get_action_str(last_action) == ACTION.DISCARD_ACTION:
            #draw
            if num_stoke_pile > 0:
                legal_actions.append(draw_card_action_id)
            
        if last_action is None or get_action_str(last_action) == ACTION.DISCARD_ACTION:
            #take
            temp_hand = current_hand + discard_pile
            _melds = get_all_melds(temp_hand)
            for meld in _melds:
                hand_card = [card for card in meld if card in current_hand]
                if len(hand_card) > 0 and len(hand_card) < len(meld) and len(hand_card) < len(current_hand):
                    #add action
                    ranks  = ",".join([str(c) for c in sorted(meld, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                    legal_actions.append(ID_2_ACTION.index(ranks) + take_card_action_id)

        if get_action_str(last_action) == ACTION.DRAW_CARD_ACTION or \
            get_action_str(last_action) == ACTION.DEPOSIT_CARD_ACTION or \
            get_action_str(last_action) == ACTION.MELD_CARD_ACTION or \
            get_action_str(last_action) == ACTION.TAKE_CARD_ACTION:

            #discard
            discard_actions = [card_id + discard_action_id for card_id in current_hand]
            legal_actions = discard_actions + legal_actions

        if get_action_str(last_action) == ACTION.DRAW_CARD_ACTION or \
            get_action_str(last_action) == ACTION.DEPOSIT_CARD_ACTION or \
            get_action_str(last_action) == ACTION.MELD_CARD_ACTION or \
            get_action_str(last_action) == ACTION.TAKE_CARD_ACTION:
            #meld

            if len(current_hand) > 3 and len(current_melds)> 0:
                __melds = get_all_melds(current_hand)
                for meld in __melds:
                    if len(meld) < len(current_hand): 
                        ranks  = ",".join([str(c) for c in sorted(meld, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                        legal_actions.append(ID_2_ACTION.index(ranks) + meld_card_action_id)

        if get_action_str(last_action) == ACTION.DRAW_CARD_ACTION or \
            get_action_str(last_action) == ACTION.DEPOSIT_CARD_ACTION or \
            get_action_str(last_action) == ACTION.MELD_CARD_ACTION or \
            get_action_str(last_action) == ACTION.TAKE_CARD_ACTION:
            #deposit
            if len(current_hand) > 1 and len(current_melds) > 0:
                for card_id in current_hand:
                    for meld in all_melds:
                        meld_check = meld + [card_id]
                        if is_meld(meld_check):
                            ranks  = ",".join([str(c) for c in sorted(meld, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                            legal_actions.append(ID_2_ACTION.index(ranks) + deposit_card_action_id)

        if get_action_str(last_action) == ACTION.DEPOSIT_CARD_ACTION  or\
            get_action_str(last_action) == ACTION.MELD_CARD_ACTION or \
            get_action_str(last_action) == ACTION.TAKE_CARD_ACTION:
            
            if len(current_hand) == 1:
                return [knock_action_id + current_hand[0]]

        if  get_action_str(last_action) == ACTION.DISCARD_ACTION:
            if num_stoke_pile == 0:
                return [knock_action_id + 52]
        
        return legal_actions