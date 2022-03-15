from rlcard.games.dummy.action_event import ActionEvent, KnockAction
import numpy as np
from rlcard.games.dummy.judge import DummyJudge
from rlcard.games.dummy.player import DummyPlayer

from rlcard.games.dummy.round import DummyRound


class DummyGame:
    def __init__(self) -> None:
        self._num_player = 2
        self.np_random = np.random.RandomState()
        self.judge = DummyJudge(game = self)
        self.round = None

    def init_game(self):
        dealer_id : int = self.np_random.choice([0, 1])
        self.actions = []
        self.round = DummyRound(dealer_id=dealer_id, num_players=self._num_player, np_random=self.np_random)
        for i in range(self._num_player):
            if self._num_player == 2:
                num = 11
            elif self._num_player == 3:
                num = 9
            else:
                num = 7

            player = self.round.players[(dealer_id + 1 + i) % 2]
            self.round.dealer.deal_cards(player=player, num=num)

        self.round.dealer.deal_first_card()

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
        if isinstance(action, KnockAction):
            self.round.knock(action)
        else:
            raise Exception('Unknown step action={}'.format(action))

        self.actions.append(action)

        next_player_id = self.round.current_player_id
        next_state = self.get_state(player_id=next_player_id)
        return next_state, next_player_id 