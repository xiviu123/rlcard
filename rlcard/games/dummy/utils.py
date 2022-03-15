from typing import List
from rlcard.games.base import Card
from .dummy_error import DummyProgramError
import numpy as np
import rlcard
import os

ROOT_PATH = rlcard.__path__[0]


# Action space
action_space_path = os.path.join(ROOT_PATH, 'games/dummy/jsondata/meld_action.txt')
with open(action_space_path, 'r') as f:
    ID_2_ACTION = f.readline().strip().split()
    ACTION_2_ID = {}
    for i, action in enumerate(ID_2_ACTION):
        ACTION_2_ID[action] = i


valid_rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
valid_suit = ['S', 'H', 'D', 'C']

def card_from_card_id(card_id: int) -> Card:
    ''' Make card from its card_id
    Args:
        card_id: int in range(0, 52)
     '''
    if not (0 <= card_id < 52):
        raise DummyProgramError("card_id is {}: should be 0 <= card_id < 52.".format(card_id))
    rank_id = card_id % 13
    suit_id = card_id // 13
    rank = valid_rank[rank_id]
    suit = valid_suit[suit_id]
    return Card(rank=rank, suit=suit)

_deck = [card_from_card_id(card_id) for card_id in range(52)]  # want this to be read-only

def get_deck() -> List[Card]:
    return _deck.copy()

def get_card_id(card: Card) -> int:
    rank_id = get_rank_id(card)
    suit_id = get_suit_id(card)
    return rank_id + 13 * suit_id

def get_rank_id(card: Card) -> int:
    return valid_rank.index(card.rank)


def get_suit_id(card: Card) -> int:
    return valid_suit.index(card.suit)

def encode_cards(cards: List[Card]) -> np.ndarray:
    plane = np.zeros(52, dtype=int)
    for card in cards:
        card_id = get_card_id(card)
        plane[card_id] = 1
    return plane

def encode_melds(melds: List[str]):
    plane = np.zeros(329, dtype=int)
    for meld in melds:
        meld_id = ID_2_ACTION[meld]
        plane[meld_id] = 1

    return plane

def get_card(card_id: int):
    return _deck[card_id]

rank_to_deadwood_value = {"A": 15, "2": 5, "3": 5, "4": 5, "5": 5, "6": 5, "7": 5, "8": 5, "9": 5,
                          "T": 10, "J": 10, "Q": 10, "K": 10}
                          
def get_deadwood_value(card: Card, speto_cards: List[Card]) -> int:
    rank = card.rank
    deadwood_value = rank_to_deadwood_value.get(rank, 10)  # default to 10 is key does not exist
    if card in speto_cards:
        deadwood_value  = deadwood_value + 50
    return deadwood_value