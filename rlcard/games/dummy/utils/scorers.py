from typing import Callable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import DummyGame
from ..player import DummyPlayer
from ..utils import utils as utils

class DummyScorer:
    def __init__(self, name: str = None, get_payoff: Callable[[DummyPlayer, 'DummyGame'], int or float] = None) -> None:
        self.name = name if name is not None else "DummyScorer"
        self.get_payoff = get_payoff if get_payoff else self.get_payoff_dummy

    def get_payoffs(self, game: 'DummyGame'):
        payoffs = [0, 0]
        for i in range(game.num_players):
            player = game.round.players[i]
            payoff = self.get_payoff(player, game)
            payoffs[i] = payoff
        return payoffs

    def get_payoff_dummy(self, player: DummyPlayer, game: 'DummyGame') -> int:
        ''' Get the payoff of player:
                a) 1.0 if player gins
                b) 0.2 if player knocks
                c) -deadwood_count / 100 otherwise

        Returns:
            payoff (int or float): payoff for player (higher is better)
        '''
        score =  player.score - sum([utils.get_deadwood_value(card, game.round.dealer.speto_cards) for card in player.hand])
        
        for card_id in game.round.card_meld_by_player:
            if game.round.card_meld_by_player[card_id] == player.player_id:
                card = utils.get_card(card_id)
                score = score + utils.get_deadwood_value(card, game.round.dealer.speto_cards)

        # payoff is 1.0 if player gins
        # payoff is 0.2 if player knocks
        # payoff is -deadwood_count / 100 if otherwise
        # The goal is to have the agent learn how to knock and gin.
        # The negative payoff when the agent fails to knock or gin should encourage the agent to form melds.
        # The payoff is scaled to lie between -1 and 1.
        return score