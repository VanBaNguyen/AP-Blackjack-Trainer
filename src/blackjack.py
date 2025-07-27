from shoe import Shoe

def card_value(card):
    rank = card[0]
    if rank in 'TJQK':
        return 10
    elif rank == 'A':
        return 1
    else:
        return int(rank)

def hand_value(hand):
    """Returns tuple (value, is_soft)"""
    value = sum(card_value(card) for card in hand)
    num_aces = sum(1 for card in hand if card[0] == 'A')
    # Try to convert aces from 1 to 11 if possible (soft hand)
    is_soft = False
    while num_aces > 0 and value + 10 <= 21:
        value += 10
        is_soft = True
        num_aces -= 1
    return value, is_soft

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand)[0] == 21

class PlayerHand:
    def __init__(self, bet, cards=None, doubled=False):
        self.cards = cards or []
        self.bet = bet
        self.doubled = doubled
        self.finished = False  # finished = stood, busted, blackjack, or after doubling

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0][0] == self.cards[1][0]

    def can_double(self):
        return len(self.cards) == 2 and not self.doubled

    def add_card(self, card):
        self.cards.append(card)

    def is_bust(self):
        return hand_value(self.cards)[0] > 21

    def is_blackjack(self):
        return is_blackjack(self.cards)

    def value(self):
        return hand_value(self.cards)[0]

    def is_soft(self):
        return hand_value(self.cards)[1]
