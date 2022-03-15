from rlcard.games.dummy.action_event import KnockAction
from .dealer import DummyDealer
from .move import DealHandMove, KnockMove
from .player import DummyPlayer


class DummyRound:
    def __init__(self, dealer_id: int, num_players: int, np_random) -> None:
        self.np_random = np_random
        self.dealer_id = dealer_id
        self.num_players = num_players
        self.dealer = DummyDealer(self.np_random)
        self.players = [DummyPlayer(player_id=id, np_random=self.np_random) for id in range(num_players) ]
        self.current_player_id = (dealer_id + 1) % num_players
        self.is_over = False
        self.move_sheet = []  # type: List[DummyMove]
        player_dealing = DummyPlayer(player_id=dealer_id, np_random=self.np_random)
        shuffled_deck = self.dealer.shuffled_deck
        self.move_sheet.append(DealHandMove(player_dealing=player_dealing, shuffled_deck=shuffled_deck))

    def get_current_player(self) -> DummyPlayer or None:
        current_player_id = self.current_player_id
        return None if current_player_id is None else self.players[current_player_id]


    def knock(self, action : KnockAction):
        current_player = self.players[self.current_player_id]
        card = action.card
        if card is not None:
            current_player.remove_card_from_hand(action.card)
        self.move_sheet.append(KnockMove(current_player, action))
        self.is_over = True