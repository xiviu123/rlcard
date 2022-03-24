from typing import List
import numpy as np
import os
import rlcard
from .melding import get_card, get_card_str

ROOT_PATH = rlcard.__path__[0]


melds_id_path = os.path.join(ROOT_PATH, 'games/dummy/jsondata/meld_id.txt')
with open(melds_id_path, 'r') as f:
    ID_2_ACTION = f.readline().strip().split()


def get_one_hot_array(num_left_cards, max_num_cards):
    one_hot = np.zeros(max_num_cards, dtype=np.int8)

    if num_left_cards >= 1:
        one_hot[num_left_cards - 1] = 1
    return one_hot

def encode_cards(cards) -> np.ndarray:
    plane = np.zeros(52, dtype=int)
    for card_id in cards:
        plane[card_id] = 1
    return plane

def meld_2_str(meld : List[int]):
    return "".join([get_card_str(card_id) for card_id in meld])