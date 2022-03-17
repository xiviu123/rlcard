from typing import List
from .utils import get_card_id, get_rank_id

from rlcard.games.base import Card
def get_all_melds(hand: List[Card]) -> List[List[Card]]:
    return  get_all_run_melds(hand) + get_all_set_melds(hand)

def get_all_run_melds(hand: List[Card]) -> List[List[Card]]:
    card_count = len(hand)
    hand_by_suit = sorted(hand, key=get_card_id)
    max_run_melds = []

    i = 0
    while i < card_count - 2:
        card_i = hand_by_suit[i]
        j = i + 1
        card_j = hand_by_suit[j]
        while get_rank_id(card_j) == get_rank_id(card_i) + j - i and card_j.suit == card_i.suit:
            j += 1
            if j < card_count:
                card_j = hand_by_suit[j]
            else:
                break
        max_run_meld = hand_by_suit[i:j]
        if len(max_run_meld) >= 3:
            max_run_melds.append(max_run_meld)
        i = j

    result = []
    for max_run_meld in max_run_melds:
        max_run_meld_count = len(max_run_meld)
        for i in range(max_run_meld_count - 2):
            for j in range(i + 3, max_run_meld_count + 1):
                result.append(max_run_meld[i:j])
    return result


def get_all_set_melds(hand: List[Card]) -> List[List[Card]]:
    max_set_melds = []
    hand_by_rank = sorted(hand, key=lambda x: x.rank)
    set_meld = []
    current_rank = None
    for card in hand_by_rank:
        if current_rank is None or current_rank == card.rank:
            set_meld.append(card)
        else:
            if len(set_meld) >= 3:
                max_set_melds.append(set_meld)
            set_meld = [card]
        current_rank = card.rank
    if len(set_meld) >= 3:
        max_set_melds.append(set_meld)
    result = []
    for max_set_meld in max_set_melds:
        result.append(max_set_meld)
        if len(max_set_meld) == 4:
            for meld_card in max_set_meld:
                result.append([card for card in max_set_meld if card != meld_card])
    return result

def check_can_deposit(card : Card, meld: List[Card]):
    if len(meld) < 3:
        return False
    meld = sorted(meld, key=get_card_id)
    if meld[0].rank == meld[1].rank: # set
        return meld[0].rank == card.rank
         
    else:
        return  (get_rank_id(meld[0]) == get_rank_id(card) + 1  or get_rank_id(meld[len(meld) - 1]) == get_rank_id(card) - 1) and meld[0].suit == card.suit

    
