from rlcard.envs import Env
from rlcard.games.dummy.game import DummyGame as Game
import numpy as np
from rlcard.games.dummy.utils import *
from collections import OrderedDict

class DummyEnv(Env):
    ''' Dummy Environment
    '''

    def __init__(self, config):
        self.name = "dummy"
        self.game = Game()

        super().__init__(config=config)
        if self.num_players == 2:
            self.state_shape = [[987] for _ in range(self.num_players)]
        elif self.num_players == 3:
            self.state_shape = [[1408] for _ in range(self.num_players)]

        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: 
                        num_stoke_pile: Số bài trên lọc (29)
                        opponent_card_left: Số bài đối thủ còn lại (29)
                        current_hand: Bài trên tay (52)
                        current_card_left: Số bài trên tay còn lại (29)
                        known_cards: Bài lộ của đối thủ (52)
                        unknown_cards : Bài dưới lọc + bài đối thủ chưa lộ (52)
                        speto_card: 52
                        current_score_cards: Cây bài điểm (52)
                        opponent_score_cards: Cây bài điểm (52)
                        speto_card: First card (52)
                        just_discard: Bài vừa đánh (52)
                        depositable_cards : card có thể gửi (52)
        '''
        if self.game.is_over():
            if self.num_players == 2:
                obs =  np.zeros(987, dtype=int)
            elif self.num_players == 3:
                obs =  np.zeros(1408, dtype=int)
            extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions()}
            extracted_state['raw_legal_actions'] = list(self._get_legal_actions().keys())
            extracted_state['raw_obs'] = state
        else:
            num_stoke_pile  = state['num_stoke_pile']

            up_opponent_card_left = state['up_opponent_card_left']
            up_opponent_meld = state['up_opponent_meld']
            up_opponent_hand = state['up_opponent_hand']

            if self.num_players > 2:
                down_opponent_card_left = state['down_opponent_card_left']
                down_opponent_meld = state['down_opponent_meld']
                down_opponent_hand = state['down_opponent_hand']

            current_hand = state['current_hand']
            current_meld = state['current_meld']

            discard_pile = state['discard_pile']
            known_cards = state['known_cards']
            speto_card = state['speto_card']



            num_stoke_pile_rep = get_one_hot_array(num_stoke_pile,29)
            up_opponent_card_left_rep = get_one_hot_array(up_opponent_card_left, 40)
            up_opponent_meld_rep = encode_melds( up_opponent_meld)
            up_opponent_hand_rep = encode_cards(up_opponent_hand)

            if self.num_players > 2:
                down_opponent_card_left_rep = get_one_hot_array(down_opponent_card_left, 40)
                down_opponent_meld_rep = encode_melds( down_opponent_meld)
                down_opponent_hand_rep = encode_cards(down_opponent_hand)

            current_hand_rep = encode_cards(current_hand)
            current_meld_rep = encode_melds(current_meld)

            discard_pile_rep = encode_cards(discard_pile)
            known_cards_rep = encode_cards(known_cards)
            speto_card_rep = encode_cards(speto_card)


            if self.num_players == 2:
                obs = np.concatenate((
                    num_stoke_pile_rep,
                    up_opponent_card_left_rep,
                    up_opponent_meld_rep,
                    up_opponent_hand_rep,
                    current_hand_rep,
                    current_meld_rep,
                    discard_pile_rep,
                    known_cards_rep,
                    speto_card_rep
                ))
            elif self.num_players > 2:
                obs = np.concatenate((
                    num_stoke_pile_rep,
                    up_opponent_card_left_rep,
                    up_opponent_meld_rep,
                    up_opponent_hand_rep,
                    down_opponent_card_left_rep,
                    down_opponent_meld_rep,
                    down_opponent_hand_rep,
                    current_hand_rep,
                    current_meld_rep,
                    discard_pile_rep,
                    known_cards_rep,
                    speto_card_rep
                ))

            extracted_state = OrderedDict({'obs': obs, 'legal_actions': self._get_legal_actions()})
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = list(self._get_legal_actions().keys())
        return extracted_state

    def _get_legal_actions(self):
        ''' Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.judge.get_legal_actions()
        legal_actions_ids =  {action: None for action in legal_actions}
        return OrderedDict(legal_actions_ids)


    def _decode_action(self, action_id: int):
        return action_id

    def get_payoffs(self):

        is_game_complete = False
        if self.game.round:
            if self.game.is_over():
                is_game_complete = True
        payoffs = [0 for _ in range(self.num_players)] if not is_game_complete else self.game.judge.get_payoffs()
        return np.array(payoffs)
