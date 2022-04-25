import numpy as np
from rlcard.games.tienlen.player import TienlenPlayer as Player
from rlcard.games.tienlen.judger import TienlenJudger as Judger
from rlcard.games.tienlen.round import TienlenRound as Round
from .action_event import ActionEvent
class TienlenGame:
    actions_history: list
    def __init__(self) -> None:
        self.num_players = 2
        self.np_random = np.random.RandomState()
        self.actions_history = []

    def init_game(self, allow_step_back = False):
         # initialize public variables
        self.allow_step_back = allow_step_back
        self.winner_id = None
        self.history = []
        

        dealer_id : int = self.np_random.choice([i for i  in range(self.num_players)])
                    
        # self.played_cards = [np.zeros((len(CARD_RANK_STR), ), dtype=np.int) for _ in range(self.num_players)]

        self.round = Round(self.np_random, dealer_id, self.num_players)
        #deal card 
        self.round.dealer.deal_cards(self.round.players)

        # initialize judger
        self.judger = Judger(self)

        


        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def step(self, action):
        ''' Perform one draw of the game

        Args:
            action (str): specific action of doudizhu. Eg: '33344'

        Returns:
            dict: next player's state
            int: next player's id
        '''
        if self.allow_step_back:
            # TODO: don't record game.round, game.players, game.judger if allow_step_back not set
            pass

        next_id = self.round.get_next_id()

        # perfrom action
        player = self.round.players[self.round.current_player_id]
        self.round.proceed_round(player, action)
        if (action != 'pass'):
            self.judger.calc_playable_cards(player)

        else:
            self.round.player_pass(player)
            
            

        if self.judger.judge_game(self.round.players, self.round.current_player_id):
            self.winner_id = self.round.current_player_id
            self.round.add_play_score_2_result()

        self.actions_history.append(action)


        print("user : {}, action: {}".format(player.player_id, action))

        self.round.current_player_id = next_id

        # get next state
        state = self.get_state(next_id)
        self.state = state

        return state, next_id


    def get_state(self, player_id):
        player = self.round.players[player_id]

        current_hand = player.hand
        unknown_cards = self.round.dealer.deck + [c for p in self.round.players for c in p.hand]

        played_cards = [[c for action in p.actions_history if action != "pass" for c in action.cards] for p in self.round.players]
        

        num_cards_left = [len(p.hand) for p in self.round.players]
        if self.is_over():
            actions = []
        else:
            actions = list(player.available_actions(self.round.greater_player, self.judger))

        state = {
            "actions": actions,
            "player_id": player_id,
            "current_hand": current_hand,
            "played_cards": played_cards,
            "players_round_active": self.round.players_active,
            "unknown_cards": unknown_cards,
            "num_cards_left": num_cards_left,
        }

        return state

    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        return self.winner_id is not None

    def get_num_players(self):
        return self.num_players

    def get_num_actions(self):
        return ActionEvent.get_num_actions()

    def get_player_id(self):
        ''' Return current player's id

        Returns:
            int: current player's id
        '''
        return self.round.current_player_id

