from typing import List

RANK_STR = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUIT_STR = ['S', 'C', 'D', 'H']

def get_card(card_id : int):
    rank_id = card_id % 13
    suit_id = int((card_id - rank_id) / 13)
    return (rank_id, suit_id)

def get_cardid_from_card(card: tuple):
    (rank_id, suit_id) = card
    return rank_id + suit_id * 13

def get_card_str(card_id: int):
    (rank_id, suit_id) = get_card(card_id)
    return RANK_STR[rank_id] + SUIT_STR[suit_id]
    
def get_suit_id(card_id: int):
    (_, suit_id) = get_card(card_id=card_id)
    return suit_id

def get_rank_id(card_id: int):
    (rank_id, _) = get_card(card_id=card_id)
    return rank_id

def get_all_melds(cards : List[int]):
    return get_all_run_melds(cards) + get_all_set_melds(cards)

def get_all_run_melds(cards : List[int]):
    card_count = len(cards)
    hand_by_suit = sorted(cards, key=lambda x: (get_suit_id(x), get_rank_id(x)))
    max_run_melds = []

    i = 0
    while(i < card_count - 2):
        card_i = hand_by_suit[i]
        j = i + 1
        card_j = hand_by_suit[j]

        while get_rank_id(card_j) == get_rank_id(card_i) + j - i and get_suit_id(card_i) == get_suit_id(card_j):
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

def get_all_set_melds(cards: List[int]):
    hand_by_rank  = sorted(cards, key=get_rank_id)

    max_set_melds = []
    current_rank = None
    set_meld = []

    for card_id in hand_by_rank:
        if current_rank is None or current_rank == get_rank_id(card_id):
            set_meld.append(card_id)
        else:
            if len(set_meld) >= 3:
                max_set_melds.append(set_meld)
            set_meld = [card_id]
        current_rank = get_rank_id(card_id)

    if len(set_meld) >= 3:
        max_set_melds.append(set_meld)

    result = []
    for max_set_meld in max_set_melds:
        result.append(max_set_meld)
        if len(max_set_meld) == 4:
            for meld_card in max_set_meld:
                result.append([card for card in max_set_meld if card != meld_card])
    return result

def is_meld(cards: List[int]):
    return is_run_meld(cards) or is_set_meld(cards)

def is_run_meld(cards: List[int]):
    meld = sorted(cards, key=get_rank_id)
    
    i = 0
    while(i < len(meld) - 1):
        j = i+1
        if get_rank_id(meld[i]) + 1 != get_rank_id(meld[j]):
            return False
        if get_suit_id(meld[i]) != get_suit_id(meld[j]):
            return False
        i = i+1

    return True

def is_set_meld(cards: List[int]):

    i = 0
    while(i < len(cards) - 1):
        j = i+1
        if get_rank_id(cards[i])  != get_rank_id(cards[j]):
            return False
        i = i+1
    
    return True

def caculate_depositable_cards(all_melds):
    # all_melds = [meld for p in self.players for meld in p.melds]

    if len(all_melds) == 0:
        return []

    all_cards_in_melds = [card_id for meld in all_melds for card_id in meld]

    live_cards = [card_id for card_id in [i for i in range(52)] if card_id not in all_cards_in_melds]

    
    return [c for meld in all_melds for c in find_card_can_deposit(meld) if c  in live_cards]

def find_card_can_deposit(meld: List[int]):
    can_deposit = []
    if is_set_meld(meld):
        if len(meld) >= 4:
            return []
        else:
            rank_id = get_rank_id(meld[0])
            suits = [get_suit_id(c)  for c in meld]

            suit = [s for s in [0,1,2,3] if s not in suits]

            if len(suit) == 1:
                return [get_cardid_from_card((rank_id, suit[0]))]
    elif is_run_meld(meld):
        sorted_meld = sorted(meld, key=lambda x: (get_suit_id(x), get_rank_id(x)))
        suit_id = get_suit_id(meld[0])

        if get_rank_id(sorted_meld[0]) > 0:
            rank_id = get_rank_id(sorted_meld[0]) - 1
            can_deposit.append( get_cardid_from_card((rank_id, suit_id)) )
        elif get_rank_id(sorted_meld[0]) < len(RANK_STR):
            rank_id = get_rank_id(sorted_meld[-1]) + 1
            can_deposit.append( get_cardid_from_card((rank_id, suit_id)) )

    return can_deposit

