from rlcard.games.dummy.dealer import DummyDealer
from rlcard.games.dummy.utils.action_event import DepositCardAction, DiscardAction, DrawCardAction, KnockAction, MeldCardAction, TakeCardAction
from rlcard.games.dummy.utils.dummy_error import DummyProgramError
from .player import DummyPlayer
from .utils.move import DealHandMove, DiscardMove, DrawCardMove, KnockMove, TakeCardMove
import numpy as np
from .utils import utils as utils

class DummyRound:

    def __init__(self, dealer_id: int, num_players: int, np_random) -> None:
        ''' Initialize the round class
            The round class maintains the following instances:
                1) dealer: the dealer of the round; dealer has stock_pile and discard_pile
                2) players: the players in the round; each player has his own hand_pile
                3) current_player_id: the id of the current player who has the move
                4) is_over: true if the round is over
                7) move_sheet: history of the moves of the player (including the deal_hand_move)
            The round class maintains a list of moves made by the players in self.move_sheet.
            move_sheet is similar to a chess score sheet.
            I didn't want to call it a score_sheet since it is not keeping score.
            I could have called move_sheet just moves, but that might conflict with the name moves used elsewhere.
            I settled on the longer name "move_sheet" to indicate that it is the official list of moves being made.
        Args:
            dealer_id: int
        '''

        self.np_random = np_random
        self.dealer_id = dealer_id
        self.num_players = num_players
        self.dealer = DummyDealer(self.np_random)
        self.players = [DummyPlayer(player_id=id, np_random=self.np_random) for id in range(num_players) ]
        self.current_player_id = (dealer_id + 1) % num_players
        self.is_over = False
        self.move_sheet = []  # type: List[DummyMove]
        player_dealing = DummyPlayer(player_id=dealer_id, np_random=self.np_random)
        shuffled_deck = self.dealer.shuffled_deck
        self.move_sheet.append(DealHandMove(player_dealing=player_dealing, shuffled_deck=shuffled_deck))
    
    def get_current_player(self) -> DummyPlayer or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]

    def draw_card(self, action: DrawCardAction):
        # when current_player takes DrawCardAction step, the move is recorded and executed
        # current_player keeps turn
        current_player = self.players[self.current_player_id]
        card = self.dealer.stock_pile.pop()

        

        self.move_sheet.append(DrawCardMove(current_player, action=action, card=card))
        current_player.add_card_to_hand(card=card)
    
    def deposit_card(self, action: DepositCardAction):
        current_player = self.players[self.current_player_id]
        cards = sorted(action.cards, key=utils.get_card_id)

        for card in cards:
            
            if card in current_player.hand:
                card_deposit = card
                current_player.remove_card_from_hand(card_deposit)
                cards.remove(card_deposit)

                if card_deposit in current_player.known_cards:
                    current_player.known_cards.remove(card_deposit)

        for meld in self.dealer.melds:
            if len(list(set(meld) - set(cards))) == 0:
                meld.append(card_deposit)
                break

    def meld_card(self, action: MeldCardAction):
        current_player = self.players[self.current_player_id]
        cards = action.cards


        # print(cards, current_player.hand)

        for card in cards:
            if card in current_player.known_cards:
                current_player.known_cards.remove(card)
            current_player.remove_card_from_hand(card)
        
        self.dealer.melds.append(cards)

    def discard(self, action: DiscardAction):
        current_player = self.players[self.current_player_id]
        self.move_sheet.append(DiscardMove(current_player, action))
        card = action.card
        current_player.remove_card_from_hand(card=card)
        if card in current_player.known_cards:
            current_player.known_cards.remove(card)
        self.dealer.discard_pile.append(card)
        self.current_player_id = (self.current_player_id + 1) % self.num_players


        for c in self.dealer.discard_pile:
            c.discard_round = c.discard_round + 1
        card.discard_round = 0
        card.discard_uid = self.current_player_id


    def takecard(self, action: TakeCardAction):
        current_player = self.players[self.current_player_id]
        self.dealer.melds.append(action.cards)
        for card in action.cards:
            if card in current_player.hand:
                current_player.hand.remove(card)

        index = -1

        # arr = np.array(self.dealer.discard_pile)
        discard  = []
        for card in action.cards:
            if card in current_player.known_cards:
                current_player.known_cards.remove(card)
            if card in self.dealer.discard_pile:
                discard.append(card)
                i = self.dealer.discard_pile.index(card)
                if index == - 1:
                    index = i
                else:
                    index = i if i < index else index

        if index > -1:
            know_cards = list(set(self.dealer.discard_pile[index: len(self.dealer.discard_pile)]) - set(discard))
            for c in know_cards:
                current_player.add_card_to_hand(c)
            current_player.known_cards = current_player.known_cards + know_cards
            self.dealer.discard_pile = self.dealer.discard_pile[0: index]

        self.move_sheet.append(TakeCardMove(current_player, action))

    def knock(self, action: KnockAction):
        # when current_player takes KnockAction step, the move is recorded and executed
        # opponent knows that the card is no longer in current_player hand
        # north becomes current_player to score his hand
        current_player = self.players[self.current_player_id]
        card = action.card
        if card is not None:
            current_player.remove_card_from_hand(action.card)
        self.move_sheet.append(KnockMove(current_player, action))
        self.is_over = True