
import math
from rlcard.games.tienlen.card import SUIT_STR, get_rank_id, get_suit_id
from rlcard.games.tienlen.utils import nCr
# from  itertools import 


action_id_pass = 0
action_id_solo = 1 #52 = nCr(4,1) * 13
action_id_pair = action_id_solo + 52                    # 78 = nCr(4,2) * 13
action_id_three_of_a_kind = action_id_pair + 78                   # 52 = nCr(4,3) * 13
action_id_four_of_a_kind = action_id_three_of_a_kind + 52                  # 13 = nCr(4,4) * 13
action_id_2_pair = action_id_four_of_a_kind + 13                 # 396 = nCr(4,2)**2 * 11
action_id_3_pair = action_id_2_pair + 396               # 2160 = nCr(4,2)**3 * 10
action_id_4_pair = action_id_3_pair + 2160              # 11664 = nCr(4,2)**4 * 9
action_id_straight_3 = action_id_4_pair + 11664         # 640 = nCr(4,1)**3 * 10
action_id_straight_4 = action_id_straight_3 + 640       # 2304 = nCr(4,1)**4 * 9
action_id_straight_5 = action_id_straight_4 + 2304      # 8192 = nCr(4,1)**5 * 8
action_id_straight_6 = action_id_straight_5 + 8192      # 28672 - 7
action_id_straight_7 = action_id_straight_6 + 28672     # 98304 - 6
action_id_straight_8 = action_id_straight_7 + 98304     # 327680 - 5
action_id_straight_9 = action_id_straight_8 + 327680    # 1048576 - 4
action_id_straight_10 = action_id_straight_9 + 1048576  # 3145728 - 3
action_id_straight_11 = action_id_straight_10 + 3145728 # 8388608 - 2
action_id_straight_12 = action_id_straight_11 + 8388608 # 16777216 - 1

pair_index = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
three_of_a_kind_index = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]

class ActionEvent:
    action_type: str
    def __init__(self, action_id: int) -> None:
        self.action_id = action_id
    @staticmethod
    def get_num_actions():
        return action_id_straight_12 + 16777216

    @staticmethod
    def get_action(type_action: str, cards = None):
            
        if type_action == "pass":
            return PassAction()
        elif type_action == "solo":
            if len(cards) != 1:
                raise Exception("cards action invalid")
            return SoloAction(cards[0])
        elif type_action == "Pair":
            if len(cards) != 2:
                raise Exception("cards action invalid")
            cards = sorted(cards)
            rank_id = get_rank_id(cards[0])
            suits = tuple([get_suit_id(c) for c in cards])
            action_id = rank_id * len(pair_index) + pair_index.index(suits)
            return PairAction(action_id)
        elif type_action == "ThreeOfAKind":
            if len(cards) != 3:
                raise Exception("cards action invalid")
            cards = sorted(cards)
            rank_id = get_rank_id(cards[0])
            suits = tuple([get_suit_id(c) for c in cards])
            action_id = rank_id * len(three_of_a_kind_index) + three_of_a_kind_index.index(suits)

            return ThreeOfAKindAction(action_id)

        elif type_action == "FourOfAKind":
            if len(cards) != 4:
                raise Exception("cards action invalid")
            
            rank_id = get_rank_id(cards[0])
            action_id = rank_id

            return FourOfAKindAction(action_id)

        elif type_action == "Chain2Pair":
            if len(cards) != 4:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x), get_suit_id(x)))
            chain_length = 2
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * len(pair_index) ** chain_length
            for i in reversed(range(chain_length)):
                suits = tuple([get_suit_id(c) for c in cards[i * 2 : i * 2 + 2]])
                action_id += pair_index.index(suits) * len(pair_index) **  (chain_length - i - 1)

            return Chain2PairAction(action_id)

        elif type_action == "Chain3Pair":
            if len(cards) != 6:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x), get_suit_id(x)))
            chain_length = 3
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * len(pair_index) ** chain_length
            for i in range(chain_length):
                suits = tuple([get_suit_id(c) for c in cards[i * 2 : i * 2 + 2]])
                action_id += pair_index.index(suits) * len(pair_index) **( chain_length - i - 1)

            
            return Chain3PairAction(action_id)

        elif type_action == "Chain4Pair":
            if len(cards) != 8:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x), get_suit_id(x)))
            chain_length = 4
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * len(pair_index) ** chain_length
            for i in range(chain_length):
                suits = tuple([get_suit_id(c) for c in cards[i * 2 : i * 2 + 2]])
                action_id += pair_index.index(suits) * len(pair_index) **( chain_length - i - 1)

            return Chain4PairAction(action_id)

        elif type_action == "Chain3":
            if len(cards) != 3:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 3
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain3Action(action_id)

        elif type_action == "Chain4":
            if len(cards) != 4:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 4
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain4Action(action_id)

        elif type_action == "Chain5":
            if len(cards) != 5:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 5
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain5Action(action_id)

        elif type_action == "Chain6":
            if len(cards) != 6:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 6
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain6Action(action_id)

        elif type_action == "Chain7":
            if len(cards) != 7:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 7
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain7Action(action_id)

        elif type_action == "Chain8":
            if len(cards) != 8:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 8
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain8Action(action_id)

        elif type_action == "Chain9":
            if len(cards) != 9:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 9
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain9Action(action_id)

        elif type_action == "Chain10":
            if len(cards) != 10:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 10
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain10Action(action_id)

        elif type_action == "Chain11":
            if len(cards) != 11:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 11
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain11Action(action_id)

        elif type_action == "Chain12":
            if len(cards) != 12:
                raise Exception("cards action invalid")
            cards = sorted(cards, key=lambda x: (get_rank_id(x)))
            chain_length = 12
            rank_id = get_rank_id(cards[0])

            action_id = rank_id * 4**chain_length
            for i in range(chain_length):
                suit = get_suit_id(cards[i])
                action_id += suit * 4 **( chain_length - i - 1)
            
            return Chain12Action(action_id)

        else:
            raise Exception("Not support type action: {}".format(type_action))

    @staticmethod
    def decode_action(action_id : int):
        if action_id == 0:
            return PassAction()
        elif action_id in range(action_id_solo, action_id_pair):
            return SoloAction(action_id - action_id_solo)
        elif action_id in range(action_id_pair, action_id_three_of_a_kind):
            return PairAction(action_id - action_id_pair)
        elif action_id in range(action_id_three_of_a_kind, action_id_four_of_a_kind):
            return ThreeOfAKindAction(action_id - action_id_three_of_a_kind)
        elif action_id in range(action_id_four_of_a_kind, action_id_2_pair):
            return FourOfAKindAction(action_id - action_id_four_of_a_kind)
        elif action_id in range(action_id_2_pair, action_id_3_pair):
            return Chain2PairAction(action_id - action_id_2_pair)
        elif action_id in range(action_id_3_pair, action_id_4_pair):
            return Chain3PairAction(action_id - action_id_3_pair)
        elif action_id in range(action_id_4_pair, action_id_straight_3):
            return Chain4PairAction(action_id - action_id_4_pair)

        elif action_id in range(action_id_straight_3, action_id_straight_4):
            return Chain3Action(action_id - action_id_straight_3)
        elif action_id in range(action_id_straight_4, action_id_straight_5):
            return Chain4Action(action_id - action_id_straight_4)
        elif action_id in range(action_id_straight_5, action_id_straight_6):
            return Chain5Action(action_id - action_id_straight_5)
        elif action_id in range(action_id_straight_6, action_id_straight_7):
            return Chain6Action(action_id - action_id_straight_6)
        elif action_id in range(action_id_straight_7, action_id_straight_8):
            return Chain7Action(action_id - action_id_straight_7)
        elif action_id in range(action_id_straight_8, action_id_straight_9):
            return Chain8Action(action_id - action_id_straight_8)
        elif action_id in range(action_id_straight_9, action_id_straight_10):
            return Chain9Action(action_id - action_id_straight_9)
        elif action_id in range(action_id_straight_10, action_id_straight_11):
            return Chain10Action(action_id - action_id_straight_10)
        elif action_id in range(action_id_straight_11, action_id_straight_12):
            return Chain11Action(action_id - action_id_straight_11)
        elif action_id in range(action_id_straight_12, action_id_straight_12 + 16777216):
            return Chain12Action(action_id - action_id_straight_12)
        else:
            raise Exception("Wrong action_id {}".format(action_id))

class PassAction(ActionEvent):

    def __init__(self):
        super().__init__(action_id=action_id_pass)

    def __str__(self):
        return "pass"

class SoloAction(ActionEvent):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id = action_id + action_id_solo)

        self.cards = [action_id]
        self.action_type = "solo"
        
    def __str__(self):
        return "solo"

class PairAction(ActionEvent):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id = action_id + action_id_pair)

        rank_id = 12
    
        while(rank_id >= 0):
            if action_id >= rank_id * len(pair_index):
                action_id = action_id - rank_id * len(pair_index)
                break
            rank_id -= 1

        self.cards = [s * 13 + rank_id for s in pair_index[action_id]]
        self.action_type = "Pair"

    def __str__(self):
        return "Pair"

class ThreeOfAKindAction(ActionEvent):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id = action_id + action_id_three_of_a_kind)

        rank_id = 12
        
    
        while(rank_id >= 0):
            if action_id >= rank_id * len(three_of_a_kind_index):
                action_id = action_id - rank_id * len(three_of_a_kind_index)
                break
            rank_id -= 1

        self.cards = [s * 13 + rank_id for s in three_of_a_kind_index[action_id]]
        self.action_type = "ThreeOfAKind"


    def __str__(self):
        return "ThreeOfAKind"

class FourOfAKindAction(ActionEvent):
    def __init__(self, action_id: int) -> None:
        if action_id > 12 or action_id < 0:
            raise Exception("FourOfAKindAction wrong action id {}". format(action_id))
        super().__init__(action_id = action_id + action_id_four_of_a_kind)

        self.cards = [s * 13 + action_id for s, _ in enumerate(SUIT_STR)]
        self.action_type = "FourOfAKind"

    def __str__(self):
        return "FourOfAKind"

class ChainPairAction(ActionEvent):
    def __init__(self, action_id: int, chain_length: int) -> None:


        action_id_mile = 0
        if chain_length == 2:
            action_id_mile = action_id_2_pair
        elif chain_length == 3:
            action_id_mile = action_id_3_pair
        elif chain_length == 4:
            action_id_mile = action_id_4_pair
        super().__init__(action_id = action_id + action_id_mile)

        rank_id = 13 - chain_length

        if action_id < 0 or action_id >= nCr(4,2)**chain_length * rank_id:
            raise Exception("ChainAction wrong action id {}". format(action_id))

        while(rank_id >= 0):
            if action_id >= rank_id * len(pair_index) ** chain_length:
                action_id = action_id - rank_id * len(pair_index) ** chain_length
                break
            rank_id -= 1

        
        suits = []
        for i in reversed(range(chain_length)):
            s = action_id // (len(pair_index)**i)
            suits.append(s)
            action_id = action_id - s * len(pair_index)**i

        self.cards = [s * 13 + rank_id + v  for v, ss in enumerate(suits) for s in pair_index[ss]]
        

class Chain2PairAction(ChainPairAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 2)
        self.action_type = "Chain{}Pair".format(2)

    def __str__(self):
        return self.action_type

class Chain3PairAction(ChainPairAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 3)
        self.action_type = "Chain{}Pair".format(3)

    def __str__(self):
        return self.action_type

class Chain4PairAction(ChainPairAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 4)
        self.action_type = "Chain{}Pair".format(4)

    def __str__(self):
        return self.action_type

class ChainAction(ActionEvent):
    def __init__(self, action_id: int, chain_length: int) -> None:
        action_id_mile = 0
        if chain_length == 3:
            action_id_mile = action_id_straight_3
        elif chain_length == 4:
            action_id_mile = action_id_straight_4
        elif chain_length == 5:
            action_id_mile = action_id_straight_5
        elif chain_length == 6:
            action_id_mile = action_id_straight_6
        elif chain_length == 7:
            action_id_mile = action_id_straight_7
        elif chain_length == 8:
            action_id_mile = action_id_straight_8
        elif chain_length == 9:
            action_id_mile = action_id_straight_9
        elif chain_length == 10:
            action_id_mile = action_id_straight_10
        elif chain_length == 11:
            action_id_mile = action_id_straight_11
        elif chain_length == 12:
            action_id_mile = action_id_straight_12
        super().__init__(action_id = action_id + action_id_mile)
        rank_id = 13 - chain_length

        if action_id < 0 or action_id >= (nCr(4,1)**chain_length) * rank_id:
            raise Exception("ChainAction wrong action id {}". format(action_id))

        while(rank_id >= 0):
            if action_id >= rank_id * 4**chain_length:
                action_id = action_id - rank_id * 4**chain_length
                break
            
            rank_id -= 1
        suits = []
        for i in reversed(range(chain_length)):
            s = action_id // (4**i)
            suits.append(s)
            action_id = action_id - s * 4**i

        self.cards = [rank_id + s + v * 13 for s, v in enumerate(suits)]
        
class Chain3Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 3)
        self.action_type = "Chain{}".format(3)

    def __str__(self):
        return self.action_type


class Chain4Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 4)
        self.action_type = "Chain{}".format(4)

    def __str__(self):
        return self.action_type

class Chain5Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 5)
        self.action_type = "Chain{}".format(5)

    def __str__(self):
        return self.action_type

class Chain6Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 6)
        self.action_type = "Chain{}".format(6)

    def __str__(self):
        return self.action_type

class Chain7Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 7)
        self.action_type = "Chain{}".format(7)

    def __str__(self):
        return self.action_type

class Chain8Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 8)
        self.action_type = "Chain{}".format(8)

    def __str__(self):
        return self.action_type

class Chain9Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 9)
        self.action_type = "Chain{}".format(9)

    def __str__(self):
        return self.action_type

class Chain10Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 10)
        self.action_type = "Chain{}".format(10)

    def __str__(self):
        return self.action_type

class Chain11Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 11)
        self.action_type = "Chain{}".format(11)

    def __str__(self):
        return self.action_type

class Chain12Action(ChainAction):
    def __init__(self, action_id: int) -> None:
        super().__init__(action_id, 12)
        self.action_type = "Chain{}".format(12)

    def __str__(self):
        return self.action_type