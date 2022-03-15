from typing import TYPE_CHECKING, List

from rlcard.games.dummy.player import DummyPlayer
from rlcard.games.dummy.utils import get_deadwood_value

from .action_event import ActionEvent,  KnockAction
if TYPE_CHECKING:
    from .game import DummyGame


class DummyJudge:
    def __init__(self, game: 'DummyGame') -> None:
        self.game = game

    def get_legal_actions(self) -> List[ActionEvent]:
        legal_actions  = []
        last_action = self.game.get_last_action()
        current_player = self.game.get_current_player()
        hand = current_player.hand

        # if last_action is None or isinstance(last_action, DiscardAction):
        return [KnockAction(None)]

        return legal_actions

    def get_payoffs(self):
        payoffs = [0, 0]
        for i in range(self.game.get_num_players()):
            player = self.game.round.players[i]
            payoff = self.get_payoff(player)
            payoffs[i] = payoff
        return payoffs 
    
    def get_payoff(self, player: DummyPlayer):
        return sum([get_deadwood_value(card, self.game.round.dealer.speto_cards) for card in player.hand])
