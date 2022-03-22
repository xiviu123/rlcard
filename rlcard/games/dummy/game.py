from .move import DealHandMove
from rlcard.games.dummy.action_event import ActionEvent, DepositCardAction, DiscardAction, DrawCardAction, KnockAction, MeldCardAction, TakeCardAction
import numpy as np
from rlcard.games.dummy.judge import DummyJudge
from rlcard.games.dummy.player import DummyPlayer

from rlcard.games.dummy.round import DummyRound
from rlcard.games.dummy.utils import get_card, get_card_id, meld_2_rank_str


class DummyGame:
    def __init__(self) -> None:
        self._num_player = 2
        self.np_random = np.random.RandomState()
        self.judge = DummyJudge(game = self)
        self.round = None
        self.add_action_call = None

    def init_game(self):
        dealer_id : int = self.np_random.choice([0, 1])
        self.actions = []
        self.round = DummyRound(dealer_id=dealer_id, num_players=self._num_player, np_random=self.np_random, add_action_call = self.add_action_call)
        move = DealHandMove(dealer_id)
        
        for i in range(self._num_player):
            if self._num_player == 2:
                num = 11
            elif self._num_player == 3:
                num = 9
            else:
                num = 7

            player = self.round.players[(dealer_id + 1 + i) % 2]
            self.round.dealer.deal_cards(player=player, num=num)

            move.hand_cards[player.player_id] = [get_card_id(c) for c in player.hand]

        move.first_card =  self.round.dealer.deal_first_card()
        move.stock_pile = self.round.dealer.stock_pile
        self.round.move_sheet.append(move)
        if self.add_action_call  is not None:
            self.add_action_call(move)

        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def get_num_players(self):
        return self._num_player

    def get_player_id(self):
        ''' Return the current player that will take actions soon
        '''
        return self.round.current_player_id

    def get_num_actions(self):
        return ActionEvent.get_num_actions()

    @staticmethod
    def decode_action(action_id) -> ActionEvent:  # FIXME 200213 should return str
        ''' Action id -> the action_event in the game.
        Args:
            action_id (int): the id of the action
        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        '''
        return ActionEvent.decode_action(action_id=action_id)

    def get_current_player(self) -> DummyPlayer or None:
        return self.round.get_current_player()

    def get_state(self, player_id: int):
        state = {}
        state['player_id'] = self.round.current_player_id
        state['hand'] = [x.get_index() for x in self.round.players[self.round.current_player_id].hand]
        return state

    def is_over(self):
        return self.round.is_over

    def get_last_action(self) -> ActionEvent or None:
        return None if len(self.actions) == 0 else self.actions[-1]

    def step(self, action: ActionEvent):
        player  = self.round.players[self.round.current_player_id]
        if isinstance(action, DrawCardAction):
            self.round.draw_card(action)
        elif isinstance(action, DepositCardAction):
            self.round.deposit_card(action)
        elif isinstance(action, MeldCardAction):
            self.round.meld_card(action)
        elif isinstance(action, TakeCardAction):
            self.round.takecard(action)
        elif isinstance(action, DiscardAction):
            self.round.discard(action)

        elif isinstance(action, KnockAction):
            self.round.knock(action)
       
        else:
            raise Exception('Unknown step action={}'.format(action))

        self.actions.append(action)

        # print("uid: {uid}, melds: {meld}, action: {action}, hand: {hand}, discard_pile: {discard_pile}, stoke_pile: {stock}, know_card= {know_card}, top_card= {top_card}".format(uid=player.player_id,meld= ",".join([meld_2_rank_str(meld) for meld in player.melds]), action=self.get_last_action(), hand=",".join([c.get_index() for c in player.hand]), discard_pile=",".join([c.get_index() for c in self.round.dealer.discard_pile]), stock=len(self.round.dealer.stock_pile), know_card = ",".join([c.get_index() for c in player.known_cards]), top_card = ",".join([get_card(card_id).get_index() for (card_id, player_id, r) in self.round.dealer.top_discard])))

        next_player_id = self.round.current_player_id
        next_state = self.get_state(player_id=next_player_id)
        return next_state, next_player_id 