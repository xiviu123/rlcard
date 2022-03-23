from rlcard.games.dummy.utils import get_card
from termcolor import colored

def elegent_form(card):
    ''' Get a elegent form of a card string

    Args:
        card (string): A card string

    Returns:
        elegent_card (string): A nice form of card
    '''
    suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣','s': '♠', 'h': '♥', 'd': '♦', 'c': '♣' }
    rank = '10' if card[1] == 'T' else card[1]

    return suits[card[0]] + rank

def print_card(cards, known_cards):
    ''' Nicely print a card or list of cards

    Args:
        card (string or list): The card(s) to be printed
    '''

    lines = [[] for _ in range(4)]

    for card in cards:
        if card is None:
            lines[0].append('┌─────────┐')
            lines[1].append('│░░░░░░░░░│')
            lines[2].append('│░░░░░░░░░│')
            lines[3].append('└─────────┘')
        else:
            elegent_card = elegent_form(get_card(card).get_index())
            suit = elegent_card[0]
            rank = elegent_card[1:]
            if len(elegent_card) == 3:
                space = ""

            else:
                space = ' '
            
            color = None if suit == "♠" or suit == "♣" else "red"
            color_known = color if card not in known_cards else "green"

            lines[0].append(colored('┌────┐', color))
            lines[1].append(colored('│{}{} │'.format(rank + suit, space), color))
            lines[2].append(colored('│    │',color))
            lines[3].append(colored('└────┘', color_known))

    for line in lines:
        print (''.join(line))