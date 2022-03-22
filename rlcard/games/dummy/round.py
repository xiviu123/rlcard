from rlcard.games.dummy.action_event import DepositCardAction, DiscardAction, DrawCardAction, KnockAction, MeldCardAction, TakeCardAction
from .dealer import DummyDealer
from .move import DealHandMove, DepositCardMove, DiscardMove, DrawCardMove, KnockMove, MeldCardMove, TakeCardMove
from .player import DummyPlayer
from .utils import check_can_deposit_speto, get_card, get_card_id, is_meld, is_run_meld, is_set_meld, rank_2_meld, ID_2_ACTION
import numpy as np
from typing import Callable


class DummyRound:
    def __init__(self, dealer_id: int, num_players: int, np_random, add_action_call) -> None:
        self.np_random = np_random
        self.dealer_id = dealer_id
        self.num_players = num_players
        self.add_action_call = add_action_call
        self.dealer = DummyDealer(self.num_players, self.np_random)
        self.players = [DummyPlayer(player_id=id, np_random=self.np_random) for id in range(num_players) ]
        self.current_player_id = (dealer_id + 1) % num_players
        self.is_over = False
        self.move_sheet = []  # type: List[DummyMove]
        # player_dealing = DummyPlayer(player_id=dealer_id, np_random=self.np_random)
        # shuffled_deck = self.dealer.shuffled_deck
        # self.move_sheet.append(DealHandMove(player_dealing=player_dealing, shuffled_deck=shuffled_deck))

    def get_current_player(self) -> DummyPlayer or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]

    def draw_card(self, action: DrawCardAction):
        # when current_player takes DrawCardAction step, the move is recorded and executed
        # current_player keeps turn
        current_player = self.players[self.current_player_id]
        card = self.dealer.stock_pile.pop()

        move = DrawCardMove(current_player, action=action, card=card)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)
        current_player.add_card_to_hand(card=card)

    def takecard(self, action: TakeCardAction):
        current_player = self.players[self.current_player_id]
        rank_id = action.rank_id
        cards = rank_2_meld(ID_2_ACTION[rank_id])
        current_player.melds.append(cards)

        # hand_cards = []
        for card in cards:
            if card in current_player.hand:
                current_player.hand.remove(card)
                # hand_cards.append(card)


        index = -1

        # arr = np.array(self.dealer.discard_pile)
        discard  = []
        for card in cards:
            if card in current_player.known_cards:
                current_player.known_cards.remove(card)
            if card in self.dealer.discard_pile:
                discard.append(card)
                i = self.dealer.discard_pile.index(card)
                if index == - 1:
                    index = i
                else:
                    index = i if i < index else index
        # Bắt lỗi đánh ra cạ speto
        # Nếu trong bộ bài ăn  có ít nhất 2 quân bài và có speto thì phạt thiền
        if len(discard) > 2:
            common_cards = set(self.dealer.speto_cards).intersection(cards) 

            # tìm thằng đánh cuối cùng tạo ra cạ để phạt tiền
            _tup = (None, None)
            for (card_id, player_id, r) in self.dealer.top_discard:
                if get_card(card_id) in discard:
                    (_pid, _r ) = _tup
                    if _pid is None:
                        _tup = (player_id, r)
                    else:
                        if(_r > r):
                            _tup = (player_id, r)
            
            (_p, _) = _tup

            for i in range(len(common_cards)):
                if _p is not None:
                    self.players[_p].add_transation(-50)        

        if index > -1:
            card_get = self.dealer.discard_pile[index:]
            # for card in card_get:
            #     if card in self.dealer.top_discard:
            #         self.dealer.top_discard.remove(card)
            know_cards = list(set(card_get) - set(discard))
            for c in know_cards:
                current_player.add_card_to_hand(c)
            current_player.known_cards = current_player.known_cards + know_cards
            self.dealer.discard_pile = self.dealer.discard_pile[0: index]

        move = TakeCardMove(current_player, action)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)

    def deposit_card(self, action: DepositCardAction):
        current_player = self.players[self.current_player_id]
        rank_id = action.rank_id

        cards = rank_2_meld(ID_2_ACTION[rank_id])

        card_deposit = None
        for card in cards:
            
            if card in current_player.hand:
                card_deposit = card
                current_player.remove_card_from_hand(card_deposit)
                cards.remove(card_deposit)

                if card_deposit in current_player.known_cards:
                    current_player.known_cards.remove(card_deposit)

        if card_deposit is not None:
            speto_cards = [s for s in self.dealer.speto_cards if s not in [card for player in self.players for meld in player.melds for card in meld] ]
            if check_can_deposit_speto(cards, card_deposit, speto_cards):
                current_player.add_transation(-40)


        for meld in [meld  for player in self.players for meld in player.melds]:
            if len(list(set(meld) - set(cards))) == 0:
                meld.append(card_deposit)
                break

        move = DepositCardMove(current_player, action)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)

    def meld_card(self, action: MeldCardAction):
        current_player = self.players[self.current_player_id]
        rank_id = action.rank_id

        cards = rank_2_meld(ID_2_ACTION[rank_id])

        # Giả thiết, nếu hạ meld mà có thể gửi speto trừ 40
        for c in self.dealer.speto_cards:
            fcards = cards + [c]
            if is_run_meld(fcards) or is_set_meld(fcards):
                current_player.add_transation(-40)
                break


        for card in cards:
            if card in current_player.known_cards:
                current_player.known_cards.remove(card)
            current_player.remove_card_from_hand(card)
        
        current_player.melds.append(cards)

        move = MeldCardMove(current_player, action)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)


    def discard(self, action: DiscardAction):
        current_player = self.players[self.current_player_id]
        card = action.card
        current_player.remove_card_from_hand(card=card)
        if card in current_player.known_cards:
            current_player.known_cards.remove(card)
        self.dealer.discard_pile.append(card)
        
        self.dealer.top_discard = [(card_id, player_id, r+1) for (card_id, player_id, r)  in self.dealer.top_discard if r < self.num_players - 1]
            
        self.dealer.top_discard.append ((get_card_id(card), self.current_player_id, 0))
        self.current_player_id = (self.current_player_id + 1) % self.num_players

        move = DiscardMove(current_player, action)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)

    def knock(self, action : KnockAction):
        current_player = self.players[self.current_player_id]
        card = action.card
        if card is not None:
            current_player.remove_card_from_hand(action.card)
            #add score if card có thể gửi
            if card  in self.dealer.speto_cards:
                current_player.add_transation(50)
            else:
                all_melds = [meld + [card] for player in self.players for meld in player.melds]
                for meld in all_melds:
                    if is_meld(meld):
                        current_player.add_transation(50)
                        break
        
        move = KnockMove(current_player, action)
        self.move_sheet.append(move)
        if self.add_action_call is not None:
            self.add_action_call(move)
        self.is_over = True