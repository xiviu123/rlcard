from typing import List
import numpy as np
from rlcard.games.dummy.action_event import ACTION, get_action
from rlcard.games.dummy.melding import get_card_str
from rlcard.games.dummy.round import DummyRound as Round
from rlcard.games.dummy.utils import meld_2_str
from .judge import DummyJudge as Judge
class DummyGame:
    actions: List[int]
    def __init__(self) -> None:
        self.np_random = np.random.RandomState()
        self.num_players = 3

        self.judge = Judge(game=self)

    def init_game(self):
        ''' Initialize all characters in the game and start round 1
        '''

        dealer_id = 0
        self.actions = []
        self.round = Round(dealer_id, self.num_players, self.np_random)

        num = 11 if self.num_players == 2 else 9 if self.num_players == 3 else 7
        for i in range(self.num_players):
            self.round.dealer.deal_cards(self.round.players[i], num)

        self.round.dealer.deal_first_card()


        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def get_state(self, player_id: int):
        player = self.round.players[player_id]
        up_opponent_id =  (player_id + 1) % self.num_players
        up_opponent = self.round.players[up_opponent_id]

        down_opponent  = None
        if self.num_players > 2:
            down_opponent_id  = player_id - 1 if  player_id >= 1 else self.num_players  - 1
            down_opponent = self.round.players[down_opponent_id]

        far_opponent = None
        if self.num_players == 4:
            far_opponent_id = player_id + 2 if player_id < self.num_players - 2 else (player_id + 2) % self.num_players
            far_opponent = self.round.players[far_opponent_id]
        
        state = {}
        state['num_stoke_pile'] = len(self.round.dealer.stock_pile)

        state['up_opponent_card_left'] = len(up_opponent.hand)
        state['up_opponent_meld'] = up_opponent.melds
        state['up_opponent_hand'] = up_opponent.known_cards

        if down_opponent is not None:
            state['down_opponent_card_left'] = len(down_opponent.hand)
            state['down_opponent_meld'] = down_opponent.melds
            state['down_opponent_hand'] = down_opponent.known_cards

        if  far_opponent is not None:
            state['far_opponent_card_left'] = len(far_opponent.hand)
            state['far_opponent_meld'] = far_opponent.melds
            state['far_opponent_hand'] = far_opponent.known_cards

        # state['min_opponent_card_lef'] = [len(player.hand) for player in self.round.players]

        state['current_hand'] = player.hand
        state['current_meld'] = player.melds 

        state['discard_pile'] = self.round.dealer.discard_pile
        state['known_cards'] = [c for p in self.round.players for c in p.known_cards]
        state['speto_card'] = self.round.dealer.speto_cards
        # state['just_discard'] = self.round.just_discard

        
        
        # state['unknown_cards'] = self.round.dealer.stock_pile + [c for c in opponent.hand if c not in opponent.known_cards]
        
        
        
        
        # state['depositable_cards'] = self.round.depositable_cards #pretrained
        state['trans'] = [player.transactions for player in self.round.players] #pretrained
        state['player_id'] = player_id #pretrained
        return state

    def get_num_actions(self):
        return 1093

    def get_num_players(self):
        return self.num_players

    def get_player_id(self):
        return self.round.current_player_id

    def get_last_action(self) -> int or None:
        return None if len(self.actions) == 0 else self.actions[-1]

    def step(self, action_id: int):
        player  = self.round.players[self.round.current_player_id]
        (action, rank_id) = get_action(action_id)
        if action == ACTION.DRAW_CARD_ACTION:
            self.round.draw_card()
        elif action == ACTION.DEPOSIT_CARD_ACTION:
            self.round.deposit_card(rank_id)
        elif action == ACTION.MELD_CARD_ACTION:
            self.round.meld_card( rank_id)
        elif action == ACTION.TAKE_CARD_ACTION:
            self.round.take_card( rank_id)
        elif action == ACTION.DISCARD_ACTION:
            self.round.discard(rank_id)

        elif action == ACTION.KNOCK_ACTION:
            self.round.knock(rank_id)
       
        else:
            raise Exception('Unknown step action={}'.format(action_id))

        self.actions.append(action_id)

        '''
        print("uid: {uid}, melds: {meld}, action: {action}, hand: {hand}, discard_pile: {discard_pile}, stoke_pile: {stock}, know_card= {know_card}, top_card= {top_card}".format(
            uid=player.player_id,
            meld= ",".join([meld_2_str(meld) for meld in player.melds]), 
            action= get_action_str(self.get_last_action()), 
            hand=",".join([get_card_str(c) for c in player.hand]), 
            discard_pile=",".join([get_card_str(c) for c in self.round.dealer.discard_pile]), 
            stock=len(self.round.dealer.stock_pile), 
            know_card = ",".join([get_card_str(c) for c in player.known_cards]), 
            top_card = ",".join([get_card_str(c) for c in self.round.just_discard])
            ))
        '''

        next_player_id = self.round.current_player_id
        next_state = self.get_state(player_id=next_player_id)
        return next_state, next_player_id

    def is_over(self):
        ''' Return whether the current game is over
        '''
        return self.round.is_over