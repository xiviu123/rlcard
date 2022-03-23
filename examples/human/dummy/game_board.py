from examples.human.dummy.player import Player
from examples.human.dummy.utils import print_card
from rlcard.games.dummy.move import DepositCardMove, DrawCardMove, DummyMove, DealHandMove, MeldCardMove, TakeCardMove, PlayerMove, DiscardMove
from rlcard.games.dummy.utils import get_card_id, rank_2_meld_id, get_card, cards_id_2_str
from termcolor import colored
from rlcard.games.dummy.action_event import ActionEvent

from .request import predict

class GameBoard:
    def __init__(self, num_player = 2) -> None:
        self.num_player = num_player

    def reset(self):
        self.players = [Player(p) for p in range(2)]
        self.speto_cards = [10, 39]
        self.stock_pile = []
        self.discard_pile = []
        self.dealer_id = None
        self.last_action = None

    def bridge(self, move : DummyMove):
        # ACTION_DRAW_CARD = "draw_card"
        # ACTION_DISCARD = "discard"
        # ACTION_TAKE_CARD = "take_card"
        # ACTION_DEPOSIT_CARD = "deposit_card"
        # ACTION_MELD_CARD = "meld_card"
        # ACTION_KNOCK = "knock_card"


        if isinstance(move, DealHandMove):
            self.reset()
            self.discard_pile.append(move.first_card)
            if move.first_card not in self.speto_cards:
                self.speto_cards.append(move.first_card)
            self.dealer_id = move.dealer_id
            self.current_player = (self.dealer_id + 1)  % self.num_player
            self.stock_pile = [get_card_id(c) for c in move.stock_pile]
            for player_id in move.hand_cards:
                self.players[player_id].hand = move.hand_cards[player_id]

            
        elif isinstance(move, DrawCardMove):
            card_id = get_card_id(move.card)
            self.players[move.player.player_id].hand.append(card_id)
            self.last_action = "draw_card"
        elif isinstance(move, DiscardMove):
            card_id = get_card_id(move.action.card)
            self.players[move.player.player_id].hand.remove(card_id)
            if card_id in self.players[move.player.player_id].known_cards:
                self.players[move.player.player_id].known_cards.remove(card_id)
            self.discard_pile.append(card_id)

            self.current_player = (self.current_player + 1)  % self.num_player

            self.last_action = "discard"
        elif isinstance(move, DepositCardMove):
            meld_d = rank_2_meld_id(move.action.rank_id)
            for card_id in meld_d:
                if card_id in self.players[move.player.player_id].hand:
                    self.players[move.player.player_id].hand.remove(card_id)
                    if card_id in self.players[move.player.player_id].known_cards:
                        self.players[move.player.player_id].known_cards.remove(card_id)
                    meld_d.remove(card_id)

            all_meld = [meld for player in self.players for meld in player.melds]
            for meld in all_meld:
                if sorted(meld) == sorted(meld_d):
                    print("vao day k")
                    meld_d.append(card_id)     

            self.last_action = "deposit_card" 

        elif isinstance(move, TakeCardMove):
            meld_t = rank_2_meld_id(move.action.rank_id)

            #add meld
            self.players[move.player.player_id].melds.append(meld_t)


            index = 100
            for card_id in meld_t:
                if card_id in self.discard_pile:
                    ind = self.discard_pile.index(card_id)
                    if ind < index:
                        index = ind
            #remove fromm discard
            if index < len(self.discard_pile):
                #add know card to hand
                take_card = self.discard_pile[index:]
                self.discard_pile = self.discard_pile[:index]

                #remove card take
                for card_id in meld_t:
                    if card_id in self.players[move.player.player_id].hand:
                        self.players[move.player.player_id].hand.remove(card_id)
                    if card_id in take_card:
                        take_card.remove(card_id)
                
                self.players[move.player.player_id].known_cards = self.players[move.player.player_id].known_cards + take_card
                self.players[move.player.player_id].hand = self.players[move.player.player_id].hand + take_card
            self.last_action = "take_card" 

        elif isinstance(move, MeldCardMove):
            meld_t = rank_2_meld_id(move.action.rank_id)

            #add meld
            self.players[move.player.player_id].melds.append(meld_t)

            #remove from hand

            for card_id in meld_t:
                self.players[move.player.player_id].hand.remove(card_id)
            
            self.last_action = "meld_card" 

        if isinstance(move, PlayerMove):
            p = "Player: {}".format(move.player.player_id + 1)

            melds = "[" +  "; ".join([cards_id_2_str(meld) for meld in self.players[move.player.player_id].melds]) + "]"

            print("{uid} play {action}, melds: {meld}".format(uid=p,meld=melds, action= "[" + move.action.__str__() + "]"))

        self.draw()


    def draw(self):
        
        color1 = None if self.current_player == 1 else "green"
        color2 = None if self.current_player == 0 else "green"
        print(colored("==================================== PLAYER_1 HAND ====================================", color1))
        print_card(self.players[0].hand, self.players[0].known_cards)

        print("==================================== DISCARDS ====================================")
        print_card(self.discard_pile, [])

        print(colored("==================================== PLAYER_2 HAND ====================================", color2))
        print_card(self.players[1].hand, self.players[1].known_cards)
       
        other_meld = "_".join([ ",".join([str(c) for c in meld]) for player in self.players if player.player_id != self.current_player for meld in player.melds])
        current_melds = "_".join([ ",".join([str(c) for c in meld]) for meld in self.players[self.current_player].melds])

        other_unknown_cards = [card_id for player in self.players for card_id in player.hand if card_id not in player.known_cards]
        unknown_cards =  ",".join([str(c) for c in self.stock_pile + other_unknown_cards]) 

        opponent_ahead_known_cards = ",".join([str(c) for c in self.players[(self.current_player + 1) % 2].known_cards])  
        other_known_cards = opponent_ahead_known_cards

        speto_cards = ",".join([str(c) for c in self.speto_cards])
        top_discard = ''

        res = self._predict(position=self.current_player, 
            num_player=self.num_player, 
            num_stoke_pile=len(self.stock_pile),
            player_hand_cards=",".join([str(c) for c in self.players[self.current_player].hand]),
            last_action= self.last_action, 
            discard_pile=",".join([str(c) for c in self.discard_pile]),
            other_melds=other_meld,
            current_melds=current_melds,
            uknown_cards=unknown_cards,
            opponent_ahead_known_cards=opponent_ahead_known_cards,
            other_known_cards=other_known_cards,
            speto_cards=speto_cards,
            top_discard=top_discard
             )
        
        
        print("[" +  ";".join([ str(r[0]) + "-" + ActionEvent.decode_action(r[0]).__str__() + "-" + str(r[1]) for r in res]) + "]")


    def _predict(self, position: int, num_player: int, num_stoke_pile: int, 
        player_hand_cards: str, last_action: str or None, 
        discard_pile: str, other_melds, current_melds, uknown_cards, opponent_ahead_known_cards, other_known_cards, speto_cards, top_discard):
        data = {'player_position': position,
                'num_player': num_player,
                'num_stoke_pile': num_stoke_pile,
                'player_hand_cards': player_hand_cards,
                'last_action': last_action,
                'discard_pile': discard_pile,
                'other_melds': other_melds,
                'current_melds': current_melds,
                'uknown_cards': uknown_cards,
                'opponent_ahead_known_cards': opponent_ahead_known_cards,
                'other_known_cards': other_known_cards,
                'speto_cards': speto_cards,
                'top_discard': top_discard}
        # print(data)
        return predict(data)
            