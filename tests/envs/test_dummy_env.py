
import unittest
import numpy as np

import rlcard
from rlcard.agents.random_agent import RandomAgent
from rlcard.games.dummy.utils.action_event import ActionEvent

class TestDummyEnv(unittest.TestCase):

    def _1test_reset_and_extract_state(self):
        env = rlcard.make('dummy')
        state, _ = env.reset()

        self.assertEqual(state['obs'].size, 208)
    
    def _1test_get_legal_actions(self):
        env = rlcard.make('dummy')
        env.set_agents([RandomAgent(env.num_actions) for _ in range(env.num_players)])
        env.reset()
        legal_actions = env._get_legal_actions()
        for legal_action in legal_actions:
            self.assertLessEqual(legal_action, env.num_actions-1)

    def _1test_step(self):
        env = rlcard.make('dummy')
        state, _ = env.reset()
        action = np.random.choice(list(state['legal_actions'].keys()))
        _, player_id = env.step(action)
        current_player_id = env.game.round.get_current_player().player_id
        self.assertEqual(player_id, current_player_id)

    # def test_decode_action(self):
    #     ActionEvent.decode_action(922)
    def test_run(self):
        env = rlcard.make('dummy')
        env.set_agents([RandomAgent(env.num_actions) for _ in range(env.num_players)])
        trajectories, payoffs = env.run(is_training=False)
        self.assertEqual(len(trajectories), 2)
        
        print(payoffs)
        # trajectories, payoffs = env.run(is_training=True)
        # for payoff in payoffs:
        #     self.assertLessEqual(-1, payoff)
        #     self.assertLessEqual(payoff, 1)

if __name__ == '__main__':
    unittest.main()