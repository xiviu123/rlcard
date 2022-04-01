from typing import TYPE_CHECKING

from rlcard.games.dummy.player import DummyPlayer
if TYPE_CHECKING:
    from .game import DummyGame
import numpy as np

from rlcard.games.dummy.action_event import ACTION, get_action
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
        
        (action, _) = get_action(last_action)

        if last_action is None or action == ACTION.DISCARD_ACTION:
            #draw
            if num_stoke_pile > 0:
                legal_actions.append(draw_card_action_id)
            
        if last_action is None or action == ACTION.DISCARD_ACTION:
            #take
            temp_hand = current_hand + discard_pile
            _melds = get_all_melds(temp_hand)
            for meld in _melds:
                hand_card = [card for card in meld if card in current_hand]
                arr_index = np.array(np.where(np.isin(discard_pile, meld))).tolist()[0]
                take_card = []
                if len(arr_index) > 0:
                    index = np.min(arr_index)
                    take_card =  [c for c in discard_pile[index:] if c not in meld]

                if len(hand_card) > 0 and len(hand_card) < len(meld) and len(hand_card) < len(current_hand) + len(take_card):
                    #add action
                    ranks  = ",".join([str(c) for c in sorted(meld, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                    legal_actions.append(ID_2_ACTION.index(ranks) + take_card_action_id)

        if action == ACTION.DRAW_CARD_ACTION or \
            action == ACTION.DEPOSIT_CARD_ACTION or \
            action == ACTION.MELD_CARD_ACTION or \
            action == ACTION.TAKE_CARD_ACTION:

            #discard
            discard_actions = [card_id + discard_action_id for card_id in current_hand]
            legal_actions = discard_actions + legal_actions

        if action == ACTION.DRAW_CARD_ACTION or \
            action == ACTION.DEPOSIT_CARD_ACTION or \
            action == ACTION.MELD_CARD_ACTION or \
            action == ACTION.TAKE_CARD_ACTION:
            #meld

            if len(current_hand) > 3 and len(current_melds)> 0:
                __melds = get_all_melds(current_hand)
                for meld in __melds:
                    if len(meld) < len(current_hand): 
                        ranks  = ",".join([str(c) for c in sorted(meld, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                        legal_actions.append(ID_2_ACTION.index(ranks) + meld_card_action_id)

        if action == ACTION.DRAW_CARD_ACTION or \
            action == ACTION.DEPOSIT_CARD_ACTION or \
            action == ACTION.MELD_CARD_ACTION or \
            action == ACTION.TAKE_CARD_ACTION:
            #deposit
            if len(current_hand) > 1 and len(current_melds) > 0:
                for card_id in current_hand:
                    for meld in all_melds:
                        meld_check = meld + [card_id]
                        if is_meld(meld_check):
                            ranks  = ",".join([str(c) for c in sorted(meld_check, key=lambda x: (get_rank_id(x), get_suit_id(x)))])
                            legal_actions.append(ID_2_ACTION.index(ranks) + deposit_card_action_id)

        if action == ACTION.DEPOSIT_CARD_ACTION  or\
            action == ACTION.MELD_CARD_ACTION or \
            action == ACTION.TAKE_CARD_ACTION:
            
            if len(current_hand) == 1:
                return [knock_action_id + current_hand[0]]

        if  action == ACTION.DISCARD_ACTION:
            if num_stoke_pile == 0:
                return [knock_action_id + 52]
        
        return legal_actions

    def get_payoffs(self):
        payoffs = [0, 0]
        for i in range(self.game.get_num_players()):
            player = self.game.round.players[i]
            payoff = self.get_payoff(player)
            payoffs[i] = payoff


        return np.array(payoffs) if payoffs == [0, 0] else np.divide(payoffs, np.abs(payoffs).max()) 

    def get_payoff(self, player: DummyPlayer):
        deadwood_score =  -sum([_get_deadwood_value(card, self.game.round.dealer.speto_cards) for card in player.hand])
        card_score = sum([_get_deadwood_value(card, self.game.round.dealer.speto_cards) for card in player.score_cards])
        tran_score = sum(player.transactions)
        return deadwood_score + card_score + tran_score

rank_to_deadwood_value = {"A": 15, "2": 5, "3": 5, "4": 5, "5": 5, "6": 5, "7": 5, "8": 5, "9": 5,
                          "T": 10, "J": 10, "Q": 10, "K": 10}
def _get_deadwood_value(card, speto_cards):
    (rank_id, _) = get_card(card)
    deadwood_value = rank_to_deadwood_value.get(rank_id, 10)  # default to 10 is key does not exist
    if card in speto_cards:
        deadwood_value  = deadwood_value + 50
    return deadwood_value