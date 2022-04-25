from re import sub
from typing import List, TYPE_CHECKING
import collections
import numpy as np
from rlcard.games.tienlen.action_event import ActionEvent, Chain10Action, Chain11Action, Chain12Action, Chain3Action, Chain4Action, Chain5Action, Chain6Action, Chain7Action, Chain8Action, Chain9Action, FourOfAKindAction, Chain4PairAction, PairAction, PassAction, SoloAction, ThreeOfAKindAction, Chain3PairAction, Chain2PairAction
if TYPE_CHECKING:
    from .game import TienlenGame

from .card import RANK_STR, get_rank_id, get_rank_str, get_suit_id
from .player import TienlenPlayer as Player
import itertools
class TienlenJudger:
    def __init__(self, game: 'TienlenGame') -> None:
        self.game = game
        self.players  = game.round.players
        # self.np_random = np_random
        self.playable_cards = [set() for _ in range(len(self.players))]

        for player in self.players:
            player_id = player.player_id
            self.playable_cards[player_id] = self.playable_cards_from_hand(player.hand)

    def get_playable_cards(self, player: Player):
        ''' Provide all legal cards the player can play according to his
        current hand.

        Args:
            player (DoudizhuPlayer object): object of DoudizhuPlayer
            init_flag (boolean): For the first time, set it True to accelerate
              the preocess.

        Returns:
            list: list of string of playable cards
        '''

        return self.playable_cards[player.player_id]

    def calc_playable_cards(self, player : Player):
        played_cards = player.played_cards

        playable_cards = self.playable_cards[player.player_id]

        arr_index = []
        for k, act in enumerate(playable_cards):
            cm = [card for card in act.cards if card in played_cards]
            if len(cm) > 0:
                arr_index.append(k)

        for i in reversed(arr_index):
            playable_cards.pop(i)

        
    
    def get_gt_cards(self, player: Player, greater_player: Player):
        
        avail_actions = ["pass"]
        playable_cards =  self.playable_cards[player.player_id]

        last_action: ActionEvent = greater_player.get_last_action()
        if  isinstance(last_action, SoloAction):
            card = last_action.cards[0]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)


            solo_actions = [p for p in playable_cards if p.action_type == "solo"]
            for action in solo_actions:
                card_target = action.cards[0]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):

                    avail_actions.append(action)

                if get_rank_str(card) == "2":
                    #chain_3_pair
                    avail_actions += [p for p in playable_cards if p.action_type == "Chain3Pair"]

                    #four_of_a_kind
                    avail_actions += [p for p in playable_cards if p.action_type == "FourOfAKind"]
        elif isinstance(last_action, PairAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            pair_actions = [p for p in playable_cards if p.action_type == "Pair"]
            for action in pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):

                    avail_actions.append(action)

                if get_rank_str(card) == "2":
                    #chain_4_pair
                    avail_actions += [p for p in playable_cards if p.action_type == "Chain4Pair"]

                    #four_of_a_kind
                    avail_actions += [p for p in playable_cards if p.action_type == "FourOfAKind"]

        elif isinstance(last_action, ThreeOfAKindAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)

            three_actions = [p for p in playable_cards if p.action_type == "ThreeOfAKind"]
            for action in three_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                if rank_target_id > rank_id:
                    avail_actions.append(action)

        elif isinstance(last_action, FourOfAKindAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)

            four_actions = [p for p in playable_cards if p.action_type == "FourOfAKind"]
            for action in four_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                if rank_target_id > rank_id:
                    avail_actions.append(action)

        elif isinstance(last_action, Chain2PairAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain2Pair"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):

                    avail_actions.append(action)

            avail_actions += [p for p in playable_cards if p.action_type == "Chain4Pair"]


        elif isinstance(last_action, Chain3PairAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain3Pair"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):

                    avail_actions.append(action)

        elif isinstance(last_action, Chain4PairAction):
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain4Pair"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):

                    avail_actions.append(action)

        elif isinstance(last_action, Chain3Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain3"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)


        elif isinstance(last_action, Chain4Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain4"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)


        elif isinstance(last_action, Chain5Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain5"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain6Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain6"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain7Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain7"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain8Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain8"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain9Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain9"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain10Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain10"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain11Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain11"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)

        elif isinstance(last_action, Chain12Action):
            same_suit_chain  = last_action.cards.count(last_action.cards[0]) == len(last_action.cards)
            card = last_action.cards[-1]
            rank_id = get_rank_id(card)
            suit_id = get_suit_id(card)

            two_pair_actions = [p for p in playable_cards if p.action_type == "Chain12"]
            for action in two_pair_actions:
                card_target = action.cards[-1]
                rank_target_id = get_rank_id(card_target)
                suit_target_id = get_suit_id(card_target)
                
                if rank_target_id > rank_id or (rank_target_id == rank_id and (suit_target_id >  suit_id or (rank_id in [0, 1, 2]))):
                    if not same_suit_chain or (same_suit_chain and action.cards.count(action.cards[0]) == len(action.cards)):
                        avail_actions.append(action)
        else:
            raise Exception("wrong type action!")

        return avail_actions

        

    @staticmethod
    def playable_cards_from_hand(current_hand : List[int]):
        ranks_list = [get_rank_id(c) for c in current_hand]
        playable_cards = []


        cards_dict = collections.defaultdict(int)
        for rank_id in ranks_list:
            cards_dict[RANK_STR[rank_id]] += 1


        cards_count = np.array([cards_dict[k] for k in RANK_STR])
        
        non_zero_indexes = np.argwhere(cards_count > 0)
        more_than_1_indexes = np.argwhere(cards_count > 1)
        more_than_2_indexes = np.argwhere(cards_count > 2)
        more_than_3_indexes = np.argwhere(cards_count > 3)
        #solo
        for c in current_hand:
            # playable_cards.append({"type": "solo", "cards": [c]})
            playable_cards.append(ActionEvent.get_action("solo", [c]))

        #pair
        for i in more_than_1_indexes:
            cards = [c for c in current_hand if get_rank_id(c) == i[0]]
            for subset in itertools.combinations(cards, 2):
                subset  = sorted(subset, key=lambda x: x)
                # playable_cards.append({"type": "pair", "cards": [c for c in subset]})
                playable_cards.append(ActionEvent.get_action("Pair", [c for c in subset]))
        
        #three_of_a_kind
        for i in more_than_2_indexes:
            cards = [c for c in current_hand if get_rank_id(c) == i[0]]
            for subset in itertools.combinations(cards, 3):
                subset  = sorted(subset, key=lambda x: x)
                # playable_cards.append({"type": "three_of_a_kind", "cards" : [c for c in subset]})
                playable_cards.append(ActionEvent.get_action("ThreeOfAKind", [c for c in subset]))
                

        #four_of_a_kind
        for i in more_than_3_indexes:
            cards = sorted([c for c in current_hand if get_rank_id(c) == i[0]], key=lambda x: x)
            # playable_cards.append({"type": "four_of_a_kind", "cards": [c for c in cards]})
            playable_cards.append(ActionEvent.get_action("FourOfAKind", [c for c in cards]))

        #pair_2_chain -- #pair_4_chain
        pair_chain_indexes = TienlenJudger.chain_indexes(more_than_1_indexes)
        for (start, count) in pair_chain_indexes:
            for chain_count in range(2, 5, 1): #length of chain 3 -> 12
                for chain_start in range(count + 1 - chain_count): # chain_start + start -> chain_count
                    ps = []
                    for i in range(chain_count):
                        px = []
                        cards = [c for c in current_hand if get_rank_id(c) == chain_start + start + i]
                        for subset in itertools.combinations(cards, 2):
                            px.append([c for c in subset])
                        ps.append(px)

                    combinations = itertools.product(*ps)
                    for combination in combinations:
                        ll = []
                        for l in combination:
                            ll += l
                        # playable_cards.append({"type": "chain{}pair".format(chain_count), "cards": ll})
                        playable_cards.append(ActionEvent.get_action("Chain{}Pair".format(chain_count), ll))

        #solo_chain_3 -- #solo_chain_12
        solo_chain_indexes = TienlenJudger.chain_indexes(non_zero_indexes)
        for (start, count) in solo_chain_indexes:
            for chain_count in range(3, 12, 1):
                for chain_start in range(count + 1 - chain_count): # chain_start + start -> chain_count
                    ps = []
                    for i in range(chain_count):
                        px = []
                        cards = [c for c in current_hand if get_rank_id(c) == chain_start + start + i]
                        for c in cards:
                            px.append(c)
                        ps.append(px)

                    combinations = itertools.product(*ps)
                    for combination in combinations:
                        playable_cards.append(ActionEvent.get_action("Chain{}".format(chain_count), [card_id for card_id in combination]))
                        # playable_cards.append({"type": "chain{}".format(chain_count), "cards" :[card_id for card_id in combination]})
                
        return playable_cards

    @staticmethod
    def judge_game(players, player_id):
        ''' Judge whether the game is over

        Args:
            players (list): list of DoudizhuPlayer objects
            player_id (int): integer of player's id

        Returns:
            (bool): True if the game is over
        '''
        player = players[player_id]
        if not player.hand:
            return True
        return False

    @staticmethod
    def chain_indexes(indexes_list):
        ''' Find chains for solos, pairs and trios by using indexes_list

        Args:
            indexes_list: the indexes of cards those have the same count, the count could be 1, 2, or 3.

        Returns:
            list of tuples: [(start_index1, length1), (start_index1, length1), ...]

        '''
        chains = []
        prev_index = -100
        count = 0
        start = None
        for i in indexes_list:
            if (i[0] >= 12): #no chains for '2BR'
                break
            if (i[0] == prev_index + 1):
                count += 1
            else:
                if (count > 1):
                    chains.append((start, count))
                count = 1
                start = i[0]
            prev_index = i[0]
        if (count > 1):
            chains.append((start, count))
        return chains


    def get_payoffs(self):
        payoffs = [0 for _ in range(self.game.get_num_players())]
        for i in range(self.game.get_num_players()):
            player = self.game.round.players[i]
            payoff = self.get_payoff(player)
            payoffs[i] = payoff

        payoffs[self.game.winner_id] = payoffs[self.game.winner_id]  + 2
        payoffs = [p / 50 for p in payoffs]

        return payoffs

    def get_payoff(self, player: Player):
        count_score =  len(player.hand) if len(player.hand) < 13 else  2 * len(player.hand)
        deadwood_score =   sum([5 if get_suit_id(c) == 0 or get_suit_id(c) == 1 else 10  for c in player.hand if get_rank_str(c) == "2"])

        played_score = self.game.round.play_score_chain.get(player.player_id)
        return played_score - count_score - deadwood_score
