class DummyPlayer:
    def __init__(self, player_id: int, np_random) -> None:
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.known_cards = []