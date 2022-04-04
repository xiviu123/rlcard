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

        self.state_shape = [[577] for _ in range(self.num_players)]
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
            obs =  np.zeros(577, dtype=int)
            extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions()}
            extracted_state['raw_legal_actions'] = list(self._get_legal_actions().keys())
            extracted_state['raw_obs'] = state
        else:
            num_stoke_pile  = state['num_stoke_pile']
            opponent_card_left = state['opponent_card_left']
            current_hand = state['current_hand']
            current_card_left = state['current_card_left']
            current_score_cards = state['current_score_cards']
            opponent_score_cards = state['opponent_score_cards']
            known_cards = state['known_cards']
            unknown_cards = state['unknown_cards']
            speto_card = state['speto_card']
            just_discard = state['just_discard']
            depositable_cards = state['depositable_cards']
            discard_pile =  state['discard_pile']

            num_stoke_pile_rep = get_one_hot_array(num_stoke_pile,29)
            opponent_card_left_rep = get_one_hot_array(opponent_card_left, 40)
            current_hand_rep = encode_cards(current_hand)
            current_card_left_rep = get_one_hot_array(current_card_left, 40)
            known_cards_rep = encode_cards(known_cards)
            unknown_cards_rep = encode_cards(unknown_cards)
            speto_card_rep = get_one_hot_array(speto_card,52)
            just_discard_rep = encode_cards(just_discard)
            depositable_cards_rep = encode_cards(depositable_cards)
            discard_pile_rep = encode_cards(discard_pile)
            current_score_cards_rep = encode_cards(current_score_cards)
            opponent_score_cards_rep = encode_cards(opponent_score_cards)

            obs = np.concatenate((
                num_stoke_pile_rep,
                opponent_card_left_rep,
                current_hand_rep,
                current_card_left_rep,
                known_cards_rep,
                unknown_cards_rep,
                speto_card_rep,
                just_discard_rep,
                depositable_cards_rep,
                discard_pile_rep,
                current_score_cards_rep,
                opponent_score_cards_rep
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
        payoffs = [0, 0] if not is_game_complete else self.game.judge.get_payoffs()
        return np.array(payoffs)
