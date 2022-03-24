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

        self.state_shape = [[5, 52] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: 
                        num_stoke_pile: Số bài trên lọc
                        opponent_card_left: Số bài đối thủ còn lại
                        current_hand: Bài trên tay
                        current_card_left: Số bài trên tay còn lại
                        known_cards: Bài lộ của đối thủ
                        unknown_cards : Bài dưới lọc + bài đối thủ chưa lộ
                        speto_card: First card 
                        just_discard: Bài vừa đánh
                        depositable_cards : card có thể gửi
        '''
        num_stoke_pile  = None
        opponent_card_left = None
        current_hand = None
        current_card_left = None
        known_cards = None
        unknown_cards = None
        speto_card = None
        just_discard = None
        depositable_cards = None

        num_stoke_pile_rep = get_one_hot_array(num_stoke_pile,29)
        opponent_card_left_rep = get_one_hot_array(opponent_card_left, 50)
        current_hand_rep = encode_cards(current_hand)
        current_card_left_rep = get_one_hot_array(current_card_left, 50)
        known_cards_rep = encode_cards(known_cards)
        unknown_cards_rep = encode_cards(unknown_cards)
        speto_card_rep = get_one_hot_array(speto_card,52)
        just_discard_rep = encode_cards(just_discard)
        depositable_cards_rep = encode_cards(depositable_cards)

        obs = np.concatenate((
            num_stoke_pile_rep,
            opponent_card_left_rep,
            current_hand_rep,
            current_card_left_rep,
            known_cards_rep,
            unknown_cards_rep,
            speto_card_rep,
            just_discard_rep,
            depositable_cards_rep
        ))

        extracted_state = OrderedDict({'obs': obs, 'legal_actions': self._get_legal_actions()})
        extracted_state['raw_obs'] = state
        # extracted_state['raw_legal_actions'] = [a for a in state['actions']]

        return extracted_state

    def _get_legal_actions(self):
        ''' Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        '''
        legal_actions = self.game.judge.get_legal_actions()
        return legal_actions

