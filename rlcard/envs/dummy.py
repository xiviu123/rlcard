from rlcard.envs import Env
import numpy as np
from collections import OrderedDict
from rlcard.games.dummy.move import KnockMove

from rlcard.games.dummy.utils import encode_cards, encode_melds, meld_2_rank





class DummyEnv(Env):
    def __init__(self, config):
        from rlcard.games.dummy.game import DummyGame as Game

        self._KnockMove = KnockMove
        self.name = 'dummy'
        self.game = Game()
        super().__init__(config=config)
        self.state_shape = [[1055] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):  # 200213 don't use state ???
        ''' Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: num_player: số người chơi [4]
                        num_stoke_pile: số quân bài trên lọc [29] 
                        current_hand: bộ bài trên tay [52]
                        discard: bộ bài dưới bán đã đánh ra [52]
                        opponent_ahead_known_cards: Những quân bài lộ của người trước mặt [52]
                        other_known_cards: Những quân bài lộ của người khác [52]
                        speto_cards: Bài speto [52]
                        top_discard: Quân bài mới đánh ra, nếu đánh ra ghép với speto thành cặp và bị ăn sẽ bị trừ điểm [52]
                        uknown_cards: Tất cả quân bài ẩn dưới lọc và trên tay người chơi khác [52]
                        current_melds: Tất cả melds của current player [329]
                        other_melds: Tất cả melds của người khác [329]

        '''
        if self.game.is_over():
            obs =  np.zeros(1055, dtype=int)
            extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions()}
            extracted_state['raw_legal_actions'] = list(self._get_legal_actions().keys())
            extracted_state['raw_obs'] = obs
        else:
            discard_pile = self.game.round.dealer.discard_pile
            stock_pile = self.game.round.dealer.stock_pile
            current_player = self.game.get_current_player()

            opponent_ahead = self.game.round.players[(current_player.player_id + 1) % self.num_players]
            opponent_ahead_known_cards = opponent_ahead.known_cards

            other_known_cards = [card for player in self.game.round.players if (player.player_id != current_player.player_id and player.player_id != current_player.player_id + 1) for card in player.hand]
            speto_cards = self.game.round.dealer.speto_cards
            top_discard = []
            uknown_cards = stock_pile + [card for opponent in self.game.round.players if opponent.player_id !=  current_player.player_id for card in opponent.hand ]
            current_melds = [meld_2_rank(meld) for meld in current_player.melds]

            other_melds = [meld_2_rank(meld) for player in self.game.round.players if (player.player_id != current_player.player_id) for meld in player.melds]

            num_player_rep = _get_one_hot_array(self.game.get_num_players(), 4)
            num_stoke_pile_rep = _get_one_hot_array(len(self.game.round.dealer.discard_pile), 29)

            hand_rep = encode_cards(current_player.hand)
            discard_rep = encode_cards(discard_pile)
            opponent_ahead_known_cards_rep = encode_cards(opponent_ahead_known_cards)
            other_known_cards_rep = encode_cards(other_known_cards)
            speto_cards_rep = encode_cards(speto_cards)
            top_discard_rep = encode_cards(top_discard)
            uknown_cards_rep = encode_cards(uknown_cards)
            current_melds_rep = encode_melds(current_melds)
            other_melds_rep = encode_melds(other_melds)


        
            
            obs = np.concatenate((
                num_player_rep,
                num_stoke_pile_rep,
                hand_rep,  
                discard_rep, 
                opponent_ahead_known_cards_rep, 
                other_known_cards_rep, 
                speto_cards_rep,
                top_discard_rep,
                uknown_cards_rep,
                current_melds_rep,
                other_melds_rep))

            legal_actions = self._get_legal_actions()
            extracted_state = {'obs': obs, 'legal_actions': legal_actions, 'raw_legal_actions': list(legal_actions.keys())}
            extracted_state['raw_obs'] = obs
        return extracted_state

    def get_payoffs(self):
        ''' Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        '''
        # determine whether game completed all moves
        is_game_complete = False
        if self.game.round:
            move_sheet = self.game.round.move_sheet
            if move_sheet and isinstance(move_sheet[-1], self._KnockMove):
                is_game_complete = True
        payoffs = [0, 0] if not is_game_complete else self.game.judge.get_payoffs()
        return np.divide(payoffs, 100)
        # return np.array(payoffs)

    def _decode_action(self, action_id):  # FIXME 200213 should return str
        ''' Action id -> the action in the game. Must be implemented in the child class.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        '''
        return self.game.decode_action(action_id=action_id)

    def _get_legal_actions(self):
        ''' Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.judge.get_legal_actions()
        legal_actions_ids = {action_event.action_id: None for action_event in legal_actions}
        return OrderedDict(legal_actions_ids)


def _get_one_hot_array(num_left_cards, max_num_cards):
    one_hot = np.zeros(max_num_cards, dtype=np.int8)
    one_hot[num_left_cards - 1] = 1

    return one_hot