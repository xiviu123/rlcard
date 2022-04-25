from enum import Enum

from rlcard.agents.human_agents.gin_rummy_human_agent.gui_gin_rummy.configurations import DISCARD_ACTION_ID
from rlcard.games.dummy.melding import get_card_str
from rlcard.games.dummy.utils import ID_2_ACTION, meld_2_str

draw_card_action_id = 0
deposit_card_action_id = draw_card_action_id + 1
take_card_action_id = deposit_card_action_id + 329
meld_card_action_id  = take_card_action_id + 329
discard_action_id = meld_card_action_id + 329
knock_action_id = discard_action_id + 52

class ACTION(Enum):
    DRAW_CARD_ACTION = "draw_card"
    DEPOSIT_CARD_ACTION = "deposit_card"
    TAKE_CARD_ACTION = 'take_card'
    MELD_CARD_ACTION = 'meld_card'
    DISCARD_ACTION = 'discard'
    KNOCK_ACTION = "knock"

    UNKNOW_ACTION = "unknow"
    
def get_action_str(action_id : int):
    (action, rank_id) = get_action(action_id)

    name = action.value
    rank_str = ""
    if action == ACTION.DRAW_CARD_ACTION:
        pass
    elif action == ACTION.DISCARD_ACTION or action == ACTION.KNOCK_ACTION :
        rank_str =  get_card_str(rank_id)
    elif  action == ACTION.DEPOSIT_CARD_ACTION or action == ACTION.MELD_CARD_ACTION or action == ACTION.TAKE_CARD_ACTION:
        rank_str = "".join([ get_card_str(int(c)) for c  in ID_2_ACTION[rank_id].split(",")])
    else:
        pass

    return name + ":" + rank_str if rank_str != "" else name

def get_action(action_id : int):
    if action_id == draw_card_action_id:
        return (ACTION.DRAW_CARD_ACTION, draw_card_action_id)
    elif action_id in range(deposit_card_action_id, take_card_action_id):
        return (ACTION.DEPOSIT_CARD_ACTION, action_id - deposit_card_action_id)
    elif action_id in range(take_card_action_id, meld_card_action_id):
        return (ACTION.TAKE_CARD_ACTION, action_id - take_card_action_id)
    elif action_id in range(meld_card_action_id, discard_action_id):
        return (ACTION.MELD_CARD_ACTION, action_id - meld_card_action_id)
    elif action_id in range(discard_action_id, knock_action_id):
        return (ACTION.DISCARD_ACTION, action_id - discard_action_id)
    elif action_id in range(knock_action_id, knock_action_id + 53):
        return (ACTION.KNOCK_ACTION, action_id - knock_action_id)
    else:
        return (ACTION.UNKNOW_ACTION, -1)
        # raise Exception('Unknown  action={}'.format(action_id))

# class ActionEvent:
#     def __init__(self, action_id: int, name: str = '') -> None:
#         self.action_id = action_id
#         self.name = name

# class DrawCardAction(ActionEvent):

#     def __init__(self):
#         super().__init__(action_id=draw_card_action_id, name= "draw_card")

#     def __str__(self):
#         return self.name

# class DiscardAction(ActionEvent):
#     def __init__(self, card_id: int):
#         super().__init__(action_id=discard_action_id + card_id, name= "discard")
#         self.card_id = card_id

#     def __str__(self):
#         return self.name

# class TakeCardAction(ActionEvent):
#     def __init__(self, rank_id: int):
#         super().__init__(action_id = take_card_action_id + rank_id, name="takecard")
#         self.rank_id = rank_id
#     def __str__(self) -> str:
#         return self.name

# class DepositCardAction(ActionEvent):

#     def __init__(self, rank_id : int):
#         super().__init__(action_id = deposit_card_action_id + rank_id, name="deposit_card")
#         self.rank_id = rank_id

#     def __str__(self) -> str:
#         return self.name

# class MeldCardAction(ActionEvent):

#     def __init__(self, rank_id :int):
        
#         super().__init__(action_id = meld_card_action_id + rank_id, name="meld_card")
#         self.rank_id = rank_id

#     def __str__(self):
#         return self.name

# class KnockAction(ActionEvent):

#     def __init__(self, card_id: int):
#         super().__init__(action_id=knock_action_id + card_id)
#         self.card_id = card_id

#     def __str__(self):
#         return self.name
