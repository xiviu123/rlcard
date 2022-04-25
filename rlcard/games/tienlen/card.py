from typing import List

RANK_STR = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
SUIT_STR = ['S', 'C', 'D', 'H']

def get_card(rank: str, suit: str) -> int:
    return RANK_STR.index(rank) + SUIT_STR.index(suit) * 13

def get_card_str(card_id: int):
    return get_rank_str(card_id) + get_suit_str(card_id)

def get_suit_id(card_id: int):
    return card_id // 13

def get_rank_id(card_id: int):
    return card_id % 13

def get_rank_str(card_id) -> str:
    return RANK_STR[get_rank_id(card_id)]

def get_suit_str(card_id) -> str:
    return SUIT_STR[get_suit_id(card_id)]

def get_card_str(card_id) :
    return get_rank_str(card_id) + get_suit_str(card_id)
# class TienlenCard:
#     valid_suit = ['S', 'C', 'D', 'H']
#     valid_rank = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']

#     def __init__(self, rank : str, suit: str) -> None:
#         self.rank_id = self.valid_rank.index(rank)
#         self.suit_id = self.valid_suit.index(suit)
        

#     def __str__(self):
#         ''' Get string representation of a card.

#         Returns:
#             string: the combination of rank and suit of a card. Eg: AS, 5H, JD, 3C, ...
#         '''
#         return self.valid_rank[self.rank_id] + self.valid_suit[self.suit_id]

#     @property
#     def card_id(self):
#         return self.rank_id + self.suit_id * 13

#     @staticmethod
#     def get_rank_suit_from_id(card_id: int):
#         rid = card_id % 13
#         sid = card_id // 13
#         return (rid, sid)


    