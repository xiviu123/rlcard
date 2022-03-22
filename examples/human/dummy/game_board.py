from examples.human.dummy.player import Player
from examples.human.dummy.utils import print_card
from rlcard.games.dummy.move import DepositCardMove, DrawCardMove, DummyMove, DealHandMove, MeldCardMove, TakeCardMove, PlayerMove, DiscardMove
from rlcard.games.dummy.utils import get_card_id, rank_2_meld_id, get_card, cards_id_2_str


class GameBoard:
    def __init__(self, num_player = 2) -> None:
        self.num_player = num_player

    def reset(self):
        self.players = [Player(p) for p in range(2)]
        self.stock_pile = []
        self.discard_pile = []
        self.dealer_id = None

    def bridge(self, move : DummyMove):
        if isinstance(move, DealHandMove):
            self.reset()
            self.discard_pile.append(move.first_card)
            self.dealer_id = move.dealer_id
            self.stock_pile = move.stock_pile
            for player_id in move.hand_cards:
                self.players[player_id].hand = move.hand_cards[player_id]
        elif isinstance(move, DrawCardMove):
            card_id = get_card_id(move.card)
            self.players[move.player.player_id].hand.append(card_id)
        elif isinstance(move, DiscardMove):
            card_id = get_card_id(move.action.card)
            self.players[move.player.player_id].hand.remove(card_id)
            self.discard_pile.append(card_id)
        elif isinstance(move, DepositCardMove):
            meld_d = rank_2_meld_id(move.action.rank_id)
            for card_id in meld_d:
                if card_id in self.players[move.player.player_id].hand:
                    self.players[move.player.player_id].hand.remove(card_id)
                    meld_d.remove(card_id)

            all_meld = [meld for player in self.players for meld in player.melds]
            for meld in all_meld:
                if sorted(meld) == sorted(meld_d):
                    print("vao day k")
                    meld_d.append(card_id)      

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
                
                self.players[move.player.player_id].hand = self.players[move.player.player_id].hand + take_card


        elif isinstance(move, MeldCardMove):
            meld_t = rank_2_meld_id(move.action.rank_id)

            #add meld
            self.players[move.player.player_id].melds.append(meld_t)

            #remove from hand

            for card_id in meld_t:
                self.players[move.player.player_id].hand.remove(card_id)
            
        if isinstance(move, PlayerMove):
            p = "You" if move.player.player_id == 0 else "BOT"

            melds = "[" +  "; ".join([cards_id_2_str(meld) for meld in self.players[move.player.player_id].melds]) + "]"

            print("{uid} play {action}, melds: {meld}".format(uid=p,meld=melds, action= "[" + move.action.__str__() + "]"))

        self.draw()


    def draw(self):

        print("==================================== HUMAN HAND ====================================")
        print_card(self.players[0].hand)

        print("==================================== DISCARDS ====================================")
        print_card(self.discard_pile)

        print("==================================== BOT HAND ====================================")
        print_card(self.players[1].hand)