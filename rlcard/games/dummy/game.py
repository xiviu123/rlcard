import numpy as np

from .judge import DummyJudge
from .round import DummyRound
from .player import DummyPlayer
from .utils.action_event import *
class DummyGame:
    def __init__(self, allow_step_back=False) -> None:
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.judge = DummyJudge(game = self)
        self.actions = None  # type: List[ActionEvent] or None # must reset in init_game
        self.round = None  # round: GinRummyRound or None, must reset in init_game
        self.num_players = 2

    def init_game(self):
        ''' Initialize all characters in the game and start round 1
        '''
        dealer_id = self.np_random.choice([0, 1])
        self.actions = []
        self.round = DummyRound(dealer_id=dealer_id, num_players=self.num_players, np_random=self.np_random)

        for i in range(self.num_players):
            if self.num_players == 2:
                num = 11
            elif self.num_players == 3:
                num = 9
            else:
                num = 7

            player = self.round.players[(dealer_id + 1 + i) % 2]
            self.round.dealer.deal_cards(player=player, num=num)

        self.round.dealer.deal_first_card()

        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def step(self, action: ActionEvent):
        ''' Perform game action and return next player number, and the state for next player
        '''

        player  = self.round.players[self.round.current_player_id]
        if isinstance(action, DrawCardAction):
            self.round.draw_card(action)
        elif isinstance(action, DepositCardAction):
            self.round.deposit_card(action)
        elif isinstance(action, MeldCardAction):
            self.round.meld_card(action)
        elif isinstance(action, DiscardAction):
            self.round.discard(action)
        elif isinstance(action, KnockAction):
            self.round.knock(action)
        elif isinstance(action, TakeCardAction):
            self.round.takecard(action)
        else:
            raise Exception('Unknown step action={}'.format(action))

        
        
        self.actions.append(action)

        # print("uid: {uid}, action: {action}, hand: {hand}, discard_pile: {discard_pile}, stoke_pile: {stock}, know_card= {know_card}, owned_meld = {owned_meld}".format(uid=player.player_id, action=self.get_last_action(), hand=",".join([c.get_index() for c in player.hand]), discard_pile=",".join([c.get_index() for c in self.round.dealer.discard_pile]), stock=len(self.round.dealer.stock_pile), know_card = ",".join([c.get_index() for c in player.known_cards]), owned_meld=",".join(["{card_id}:{uid}".format(card_id=utils.get_card(card_id).get_index(), uid=self.round.card_meld_by_player[card_id])  for card_id in self.round.card_meld_by_player])))
        next_player_id = self.round.current_player_id
        next_state = self.get_state(player_id=next_player_id)
        return next_state, next_player_id

    def get_num_players(self):
        return self.num_players
    
    def get_num_actions(self):
        ''' Return the number of possible actions in the game
        '''
        return ActionEvent.get_num_actions()

    def get_current_player(self) -> DummyPlayer or None:
        return self.round.get_current_player()

    def get_last_action(self) -> ActionEvent or None:
        return None if len(self.actions) == 0 else self.actions[-1]

    def get_player_id(self):
        ''' Return the current player that will take actions soon
        '''
        return self.round.current_player_id

    def is_over(self):
        ''' Return whether the current game is over
        '''
        return self.round.is_over

    def get_state(self, player_id: int):
        ''' Get player's state
        Return:
            state (dict): The information of the state
        '''
        state = {}
        if not self.is_over():
            discard_pile = self.round.dealer.discard_pile
            top_discard = []
            for card in discard_pile:
                if card.discard_round < self.num_players:
                    top_discard.append(card)
            meld_cards = [[c.get_index() for c in meld] for meld in self.round.dealer.melds]

            opponent_id = (player_id + 1) % self.num_players
            opponent = self.round.players[opponent_id]
            known_cards = opponent.known_cards
            unknown_cards = self.round.dealer.stock_pile + [card for card in opponent.hand if card not in known_cards]
            state['player_id'] = self.round.current_player_id
            state['hand'] = [x.get_index() for x in self.round.players[self.round.current_player_id].hand]
            state['top_discard'] = [x.get_index() for x in top_discard]
            state['meld_cards'] = meld_cards
            state['discard_pile'] = [x.get_index() for x in discard_pile]
            state['opponent_known_cards'] = [x.get_index() for x in known_cards]
            state['unknown_cards'] = [x.get_index() for x in unknown_cards]
        return state
    
    @staticmethod
    def decode_action(action_id) -> ActionEvent:  # FIXME 200213 should return str
        ''' Action id -> the action_event in the game.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        '''
        return ActionEvent.decode_action(action_id=action_id)