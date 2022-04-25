import numpy as np
from torch import le

from rlcard.games.tienlen.card import get_suit_id
from .dealer import TienlenDealer as Dealer
from .player import TienlenPlayer as Player
class TienlenRound:
    def __init__(self, np_random: np.random.RandomState, dealer_id : int, num_players: int) -> None:
        self.np_random = np_random
        self.num_players = num_players
        self.players_active = [i for i in range(num_players)]

        self.play_score_chain = {i : 0 for i in range(self.num_players)}
        self.current_play_score = []

        # initialize players
        self.players = [Player(num, self.np_random)
                        for num in range(self.num_players)]

        self.dealer = Dealer(self.np_random)
        self.current_player_id = dealer_id
        self.greater_player = None

    def proceed_round(self, player : Player, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of DoudizhuPlayer
            action (str): string of legal specific action

        Returns:
            object of DoudizhuPlayer: player who played current biggest cards.
        '''
        # self.update_public(action)
    

        if action != "pass" and (action.action_type == "Chain3Pair" or action.action_type == "Chain4Pair" or action.action_type == "FourOfAKind"):
            
            if len(self.current_play_score) == 0:
                self.current_play_score.append([{"id": self.greater_player.player_id, "act": self.greater_player.get_last_action()}])
            self.current_play_score.append[{"id": player.player_id, "act": action}]

            


        self.greater_player = player.play(action, self.greater_player)
        
        return self.greater_player
        

    def player_pass(self, player : Player):

        self.players_active.remove(player.player_id)

        if len(self.players_active) == 1:

            #reset player round active
            self.greater_player = None
            self.players_active = [i for i in range(self.num_players)]
            
            self.add_play_score_2_result()

    def add_play_score_2_result(self):
        score = 0
        for i in range(len(self.current_play_score) - 1):
            action = self.current_play_score[i].get("act")

            if action.action_type == "solo":
                score += sum([5 if get_suit_id(c) == 0 or get_suit_id(c) == 1 else 10 for c in action.cards])
               
            elif action.action_type == "Pair":
                score += sum([5 if get_suit_id(c) == 0 or get_suit_id(c) == 1 else 10 for c in action.cards])
            elif action.action_type == "Chain3Pair":
                score += 10
            elif action.action_type == "Chain4Pair":
                score += 30
            elif action.action_type == "FourOfAKind":
                score += 20
            else:
                raise Exception("Play score error")
        if len(self.current_play_score) > 1:
            first_player_id = self.current_play_score[0].get("id")
            last_player_id = self.current_play_score[-1].get("id")
            self.play_score_chain[first_player_id] = self.play_score_chain.get(first_player_id) - score
            self.play_score_chain[last_player_id] = self.play_score_chain.get(last_player_id) + score

            self.current_play_score = []

    def get_next_id(self):
        curr_index = self.players_active.index(self.current_player_id)

        next_index = (curr_index + 1) % len(self.players_active)
        next_id = self.players_active[next_index]

        return next_id