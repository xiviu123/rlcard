from typing import List
from .card import Card
import rlcard
import os
import numpy as np

from .dummy_error import DummyProgramError

ROOT_PATH = rlcard.__path__[0]


# Action space
action_space_path = os.path.join(ROOT_PATH, 'games/dummy/jsondata/meld_action.txt')
with open(action_space_path, 'r') as f:
    ID_2_ACTION = f.readline().strip().split()
    ACTION_2_ID = {}
    for i, action in enumerate(ID_2_ACTION):
        ACTION_2_ID[action] = i

def card_from_card_id(card_id: int) -> Card:
    ''' Make card from its card_id
    Args:
        card_id: int in range(0, 52)
     '''
    if not (0 <= card_id < 52):
        raise DummyProgramError("card_id is {}: should be 0 <= card_id < 52.".format(card_id))
    rank_id = card_id % 13
    suit_id = card_id // 13
    rank = Card.valid_rank[rank_id]
    suit = Card.valid_suit[suit_id]
    return Card(rank=rank, suit=suit)

# deck is always in order from AS, 2S, ..., AH, 2H, ..., AD, 2D, ..., AC, 2C, ... QC, KC
_deck = [card_from_card_id(card_id) for card_id in range(52)]  # want this to be read-only

def card_from_text(text: str) -> Card:
    if len(text) != 2:
        raise DummyProgramError("len(text) is {}: should be 2.".format(len(text)))
    return Card(rank=text[0], suit=text[1])

def get_deck() -> List[Card]:
    return _deck.copy()

def get_card(card_id: int):
    return _deck[card_id]


def get_card_id(card: Card) -> int:
    rank_id = get_rank_id(card)
    suit_id = get_suit_id(card)
    return rank_id + 13 * suit_id


def get_rank_id(card: Card) -> int:
    return Card.valid_rank.index(card.rank)


def get_suit_id(card: Card) -> int:
    return Card.valid_suit.index(card.suit)

def is_run_meld(cards: List[Card]):
    i = 0
    while(i < len(cards) - 1):
        j = i+1
        if get_rank_id(cards[i]) + 1 != get_rank_id(cards[j]):
            return False
        if cards[i].suit != cards[j].suit:
            return False
        i = i+1

    return True

def is_set_meld(cards: List[Card]):
    i = 0
    while(i < len(cards) - 1):
        j = i+1
        if get_rank_id(cards[i])  != get_rank_id(cards[j]):
            return False
        if cards[i].suit == cards[j].suit:
            return False
        i = i+1
    
    return True
def meld_2_rank(cards: List[Card]):
    cards = sorted(cards, key=get_rank_id)

    is_run = is_run_meld(cards)
    is_set = is_set_meld(cards)

    if not is_run and not is_set:
        raise DummyProgramError("meld incorrect")

    ranks = ''.join([card.rank for card in cards])
    
    if is_set and len(cards) == 3:

        valid_suilt = ['S', 'H', 'C', 'D']
        suits = [c.suit for c in cards]

        valid_suilt = list(set(valid_suilt) - set(suits))
        ranks = ranks + valid_suilt[0]
    elif is_run:
        ranks = ranks + cards[0].suit
    return ID_2_ACTION.index(ranks)
def rank_2_meld(ranks: str):
    valid_suilt = ['S', 'C', 'H', 'D']
    if ranks[0] == ranks[1] and len(ranks) == 4 and ranks[-1] != ranks[0]:
        valid_suilt.remove(ranks[-1])
        return [get_card(Card.valid_suit.index(s) * 13 + Card.valid_rank.index(ranks[0])) for s in valid_suilt]
    elif ranks[0] == ranks[1] and len(ranks) == 4 and ranks[-1] == ranks[0]:
        return [get_card(Card.valid_suit.index(s) * 13 + Card.valid_rank.index(ranks[0])) for s in valid_suilt]
    else:
        return [get_card(Card.valid_suit.index(ranks[-1]) * 13 + Card.valid_rank.index(r)) for r in ranks[:-1]]


    pass
def decode_cards(env_cards: np.ndarray) -> List[Card]:
    result = []  # type: List[Card]
    if len(env_cards) != 52:
        raise DummyProgramError("len(env_cards) is {}: should be 52.".format(len(env_cards)))
    for i in range(52):
        if env_cards[i] == 1:
            card = _deck[i]
            result.append(card)
    return result


def encode_cards(cards: List[Card]) -> np.ndarray:
    plane = np.zeros(52, dtype=int)
    for card in cards:
        card_id = get_card_id(card)
        plane[card_id] = 1
    return plane

def encode_melds(melds: List[List[Card]]) -> np.ndarray:
    plane = np.zeros([len(melds), 52], dtype=int)
    for row, cards in enumerate(melds):
        plane[row, :] = encode_cards(cards)
    plane = plane.flatten()
    return plane


rank_to_deadwood_value = {"A": 15, "2": 5, "3": 5, "4": 5, "5": 5, "6": 5, "7": 5, "8": 5, "9": 5,
                          "T": 10, "J": 10, "Q": 10, "K": 10}

def get_deadwood_value(card: Card) -> int:
    rank = card.rank
    deadwood_value = rank_to_deadwood_value.get(rank, 10)  # default to 10 is key does not exist
    if card.speto:
        deadwood_value = deadwood_value + 50
    return deadwood_value
