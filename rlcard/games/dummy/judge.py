from typing import TYPE_CHECKING, List

from rlcard.games.dummy.player import DummyPlayer
from rlcard.games.dummy.utils import get_deadwood_value

from .action_event import ActionEvent, DepositCardAction, DiscardAction, DrawCardAction,  KnockAction, MeldCardAction, TakeCardAction
if TYPE_CHECKING:
    from .game import DummyGame
from .melding import get_all_melds, check_can_deposit
from .utils import meld_2_rank


class DummyJudge:
    def __init__(self, game: 'DummyGame') -> None:
        self.game = game

    def get_legal_actions(self) -> List[ActionEvent]:
        legal_actions  = []
        last_action = self.game.get_last_action()
        current_player = self.game.get_current_player()
        hand = current_player.hand

        if last_action is None or isinstance(last_action, DiscardAction):
            # Bốc bài DrawCardAction
            if len(self.game.round.dealer.stock_pile) > 0:
                legal_actions.append(DrawCardAction())

        if last_action is None or isinstance(last_action, DiscardAction):
            # Ăn bài TakeCardAction

            temp_hand = hand + self.game.round.dealer.discard_pile
            clusters = get_all_melds(temp_hand)
            
            for cluster in clusters:
                hand_card = [] 
                discard = []

                for card in cluster:
                    if card in hand:
                        hand_card.append(card)
                    else:
                        discard.append(card)
                
                if len(hand_card) < len(cluster) and len(hand_card) < len(hand):
                    legal_actions.append(TakeCardAction(meld_2_rank(hand_card+discard)))

        if  isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, DepositCardAction) or \
            isinstance(last_action, MeldCardAction) or \
            isinstance(last_action, TakeCardAction): 
            # Dánh bài DiscardAction


            cards_to_discard = [card for card in hand]
            discard_actions = [DiscardAction(card=card) for card in cards_to_discard]
            legal_actions = legal_actions + discard_actions


        if isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, TakeCardAction) or \
            isinstance(last_action, MeldCardAction) or \
            isinstance(last_action, DepositCardAction):
            #Hạ bài MeldCardAction

            if len(hand) > 3 and len(current_player.melds) > 0:
                clusters = get_all_melds(hand)
            
                for cluster in clusters:
                    if len(cluster) < len(hand): 
                        legal_actions.append(MeldCardAction(meld_2_rank(cluster)))
            

        if isinstance(last_action, DrawCardAction) or \
            isinstance(last_action, TakeCardAction) or \
            isinstance(last_action, DepositCardAction) or \
            isinstance(last_action, MeldCardAction) :
            #Guiwr baif DepositCardAction
            if len(hand) > 1 and len(current_player.melds) > 0:
                for card in hand:
                    for meld in [meld for player in self.game.round.players for meld in player.melds]:
                        if check_can_deposit(card, meld):
                            legal_actions.append(DepositCardAction(meld_2_rank(meld + [card])))
        
            
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
        # return [KnockAction(None)]
        return legal_actions

    def get_payoffs(self):
        payoffs = [0, 0]
        for i in range(self.game.get_num_players()):
            player = self.game.round.players[i]
            payoff = self.get_payoff(player)
            payoffs[i] = payoff
        return payoffs 
    
    def get_payoff(self, player: DummyPlayer):
        deadwood_score =  -sum([get_deadwood_value(card, self.game.round.dealer.speto_cards) for card in player.hand])
        meld_score = sum([get_deadwood_value(card, self.game.round.dealer.speto_cards) for meld in player.melds for card in meld])
        tran_score = sum(player.transactions)
        return deadwood_score + meld_score + tran_score
