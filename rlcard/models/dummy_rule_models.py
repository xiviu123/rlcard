from typing import List, OrderedDict
import numpy as np
from rlcard.games.dummy.utils import melding

from rlcard.models.model import Model
import rlcard

from rlcard.games.dummy.utils.action_event import ActionEvent, DepositCardAction, DiscardAction, KnockAction, MeldCardAction, TakeCardAction
from rlcard.games.dummy.utils.card import Card
from rlcard.games.dummy.utils import utils as utils

class DummyRuleAgent(object):
    def __init__(self):
        self.use_raw = False  # FIXME: should this be True ?

    @staticmethod
    def step(state):
        legal_actions = state['legal_actions']
        actions = legal_actions.copy()
        legal_action_events = [ActionEvent.decode_action(x) for x in legal_actions]
        take_action_events = [x for x in legal_action_events if isinstance(x, TakeCardAction)]
        deposit_action_events = [x for x in legal_action_events if isinstance(x, DepositCardAction)]
        meld_action_events = [x for x in legal_action_events if isinstance(x, MeldCardAction)]
        knock_action_events = [x for x in legal_action_events if isinstance(x, KnockAction)]
        discard_action_events = [x for x in legal_action_events if isinstance(x, DiscardAction)]


        if take_action_events:
            actions = [x.action_id for x in take_action_events]
        if deposit_action_events:
            actions = [x.action_id for x in deposit_action_events]
        if meld_action_events:
            actions = [x.action_id for x in meld_action_events]
        if knock_action_events:
            actions = [x.action_id for x in knock_action_events]
        if discard_action_events:
            print("CONG HOA XA HOI CHUA NGHIA VIET NAM")
            actions = [x.action_id for x in discard_action_events]
            

        if type(actions) == OrderedDict:
            actions = list(actions.keys())
        return np.random.choice(actions)

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the agents is not trained, this function is equivalent to step function.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted by the agent
            probabilities (list): The list of action probabilities
        '''
        probabilities = []
        return self.step(state), probabilities

    @staticmethod
    def _get_best_discards(discard_action_events : List[DiscardAction], state) -> List[Card]:
        best_discards = []  # type: List[Card]
        env_hand = state['obs']
        print(state['obs'])
        # hand = utils.decode_cards(env_cards=env_hand)
        # for discard_action_event in discard_action_events:
        #     discard_card = discard_action_event.card
        #     next_hand = [card for card in hand if card != discard_card]
        #     meld_clusters = melding.get_all_melds(hand=next_hand)
        #     deadwood_counts = []


        #     deadwood_count = utils.get_deadwood_count(hand=next_hand, meld_cluster=meld_cluster)
        #     deadwood_counts.append(deadwood_count)
        #     best_deadwood_count = min(deadwood_counts,
        #                               default=utils.get_deadwood_count(hand=next_hand, meld_cluster=[]))
        #     if best_deadwood_count < final_deadwood_count:
        #         final_deadwood_count = best_deadwood_count
        #         best_discards = [discard_card]
        #     elif best_deadwood_count == final_deadwood_count:
        #         best_discards.append(discard_card)
        return best_discards

class DummyRuleModel(Model):
    ''' Gin Rummy Rule Model
    '''

    def __init__(self):
        ''' Load pre-trained model
        '''
        super().__init__()
        env = rlcard.make('dummy')
        rule_agent = DummyRuleAgent()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents