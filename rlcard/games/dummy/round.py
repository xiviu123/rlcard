from typing import List
from rlcard.games.dummy.utils import ID_2_ACTION
from .dealer import DummyDealer as Dealer
from .player import DummyPlayer as Player
from .melding import get_all_melds, is_meld, get_suit_id, get_rank_id, is_run_meld, is_set_meld, caculate_depositable_cards
import numpy as np

class DummyRound:
    just_discard: List[int]
    depositable_cards: List[int]

    def __init__(self, dealer_id: int, num_player: int, np_random) -> None:
        self.current_player_id = dealer_id
        self.np_random = np_random

        self.is_over = False

        self.dealer = Dealer(self.np_random)

        self.num_players = num_player

        self.players = [ Player(i) for i in range(num_player)]
        self.just_discard = []
        self.depositable_cards = []

    def draw_card(self):
        current_player = self.players[self.current_player_id]
        card = self.dealer.stock_pile.pop()

        current_player.add_card_to_hand(card)

    def deposit_card(self, rank_id):
        current_player = self.players[self.current_player_id]
        cards = [int(c) for c  in ID_2_ACTION[rank_id].split(",")]

        
        card_deposit = None 
        for card in cards :
            if card in current_player.hand:
                card_deposit = card
                current_player.remove_card_from_hand(card_deposit)
                cards.remove(card_deposit)

                if card_deposit in current_player.known_cards:
                    current_player.known_cards.remove(card_deposit)

        self._caculate_depositable_cards()
        #add card to meld
        all_melds = [meld for p in self.players for meld in p.melds if sorted(meld) == sorted(cards)]
        all_melds[0].append(card_deposit)
        

        if card_deposit is not None:

            #add to score cards
            current_player.score_cards.append(card_deposit)

            #Bộ mmeld vừa gủi vào có thể gửi thêm được speto, trừ điểm
            speto_cards = [c for c in self.dealer.speto_cards if c not in [card for player in self.players for meld in player.melds for card in meld] and c not in current_player.hand]

            for c in speto_cards:
                can_deposit = False
                meld_sort = sorted([c, card_deposit] + cards, key=lambda x: (get_suit_id(x), get_rank_id(x)))
                if is_meld(meld_sort):
                    if is_run_meld(meld_sort):
                        if meld_sort[0] == c or meld_sort[-1] == c:
                            can_deposit = True
                    elif is_set_meld(meld_sort):
                        can_deposit = True

                if can_deposit:
                    #TODO trừ điểm
                    # print("trừ điểm 3")
                    current_player.add_transation(-40)
                    pass
                    
        

    def meld_card(self, rank_id):
        current_player = self.players[self.current_player_id]
        cards = [int(c) for c  in ID_2_ACTION[rank_id].split(",")]

        current_player.melds.append(cards)
        #add to score cards
        for c in cards:
            current_player.score_cards.append(c)

        for c in cards:
            current_player.remove_card_from_hand(c)
            if c in current_player.known_cards:
                current_player.known_cards.remove(c)


        self._caculate_depositable_cards()

        # Giả thiết, nếu hạ meld mà có thể gửi speto trừ điểm
        speto_cards = [c for c in self.dealer.speto_cards if c not in [card for player in self.players for meld in player.melds for card in meld] and c not in current_player.hand]
        for c in speto_cards:
            can_deposit = False
            meld_sort = sorted(cards, key=lambda x: (get_suit_id(x), get_rank_id(x)))
            if is_meld(meld_sort):
                if is_run_meld(meld_sort):
                    if meld_sort[0] == c or meld_sort[-1] == c:
                        can_deposit = True
                elif is_set_meld(meld_sort):
                    can_deposit = True

                if can_deposit:
                    #TODO trừ điểm
                    # print("trừ điểm 2")
                    current_player.add_transation(-40)
                    
    def take_card(self, rank_id):
        current_player = self.players[self.current_player_id]
        cards = [int(c) for c  in ID_2_ACTION[rank_id].split(",")]

        #add to score cards
        for c in cards:
            current_player.score_cards.append(c)

        cards_in_hand =  [c for c in cards if c in current_player.hand]
        cards_in_discard = [c for c in cards if c in self.dealer.discard_pile]

        for c in cards_in_discard:
            if c in self.just_discard:
                self.just_discard.remove(c)

        current_player.melds.append(cards)

        for c in cards_in_hand:
            current_player.remove_card_from_hand(c)
            if c in current_player.known_cards:
                current_player.known_cards.remove(c)

        index = np.min(np.where(np.isin(self.dealer.discard_pile,cards_in_discard)))

        cards_take_discard = [c for c in self.dealer.discard_pile[index:] if c not in cards_in_discard]
        self.dealer.discard_pile = self.dealer.discard_pile[:index]

        for c in cards_take_discard:
            current_player.known_cards.append(c)
            current_player.add_card_to_hand(c)


        self._caculate_depositable_cards()

         # Giả thiết, nếu hạ meld mà có thể gửi speto trừ điểm
        speto_cards = [c for c in self.dealer.speto_cards if c not in [card for player in self.players for meld in player.melds for card in meld] and c not in current_player.hand]
        for c in speto_cards:
            can_deposit = False
            meld_sort = sorted(cards + [c], key=lambda x: (get_suit_id(x), get_rank_id(x)))
            if is_meld(meld_sort):
                if is_run_meld(meld_sort):
                    if meld_sort[0] == c or meld_sort[-1] == c :
                        can_deposit = True
                elif is_set_meld(meld_sort):
                    can_deposit = True

                if can_deposit:
                    #TODO trừ điểm
                    # print("trừ điểm 1")
                    current_player.add_transation(-40)

    def discard(self, card_id):
        current_player = self.players[self.current_player_id]
        #remove card bai trên tay
        current_player.remove_card_from_hand(card_id)

        #Remove card lộ
        if card_id in current_player.known_cards:
            current_player.known_cards.remove(card_id)

        #add vào bài dưới bàn
        self.dealer.discard_pile.append(card_id)


        if len(self.just_discard) > 0:
            self.just_discard.pop(0)
        self.just_discard.append(card_id)

        #Đổi lượt chơi
        self.current_player_id = (self.current_player_id + 1) % self.num_players

        #Đánh bài lỗi trừ điểm
        if card_id in self.depositable_cards:
            #TODO trừ 50 điểm
            current_player.add_transation(-50)
            # print("trừ điểm 4")
        all_melds = get_all_melds(self.dealer.discard_pile)
        for meld in all_melds:
            if card_id in meld:
                #TODO trừ 50 điểm
                current_player.add_transation(-50)
                # print("trừ điểm 5")
                break


    def knock(self, card_id):
        current_player = self.players[self.current_player_id]
        if card_id == 52:
            #hhet loc
            pass
        else:
            current_player.remove_card_from_hand(card_id)
            if card_id in self.depositable_cards or card_id in self.dealer.speto_cards:
                current_player.add_transation(50)
            
        self.is_over = True

    def _caculate_depositable_cards(self):
        all_melds = [meld for p in self.players for meld in p.melds]

        self.depositable_cards = caculate_depositable_cards(all_melds.copy())



