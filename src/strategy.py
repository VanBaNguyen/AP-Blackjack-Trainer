# strategy.py

def card_str_to_int(card):
    rank = card[0]
    if rank == 'A':
        return 1
    elif rank in 'TJQK':
        return 10
    else:
        return int(rank)

def hand_to_int_list(hand):
    """Convert a list of card codes (like ['AS', '7D']) to ints ([1, 7])"""
    # If already a list of ints, just return it
    if all(isinstance(x, int) for x in hand):
        return hand
    return [card_str_to_int(card) for card in hand]


def should_split(hand, dealer_upcard):
    """hand: list of card codes or ints (pair)
       dealer_upcard: int (1 or 11 for Ace, 2-10, or card code string like 'AS')"""
    values = hand_to_int_list(hand)
    if isinstance(dealer_upcard, str):
        dealer_upcard = card_str_to_int(dealer_upcard)
    pair_value = values[0]  # since both cards are same value
    if dealer_upcard == 1:
        dealer_upcard = 11
    if pair_value == 1:
        return True
    elif pair_value in [2, 3]:
        return 2 <= dealer_upcard <= 7
    elif pair_value == 4:
        return dealer_upcard == 5 or dealer_upcard == 6
    elif pair_value == 5:
        return False
    elif pair_value == 6:
        return 2 <= dealer_upcard <= 6
    elif pair_value == 7:
        return dealer_upcard <= 7
    elif pair_value == 8:
        return True
    elif pair_value == 9:
        return dealer_upcard <= 6 or dealer_upcard in [8, 9]
    elif pair_value == 10:
        return False
    else:
        return False

def should_double_down(hand, dealer_upcard):
    """hand: list of card codes or ints (Ace=1, 2-10)
       dealer_upcard: int or card code string"""
    values = hand_to_int_list(hand)
    if isinstance(dealer_upcard, str):
        dealer_upcard = card_str_to_int(dealer_upcard)
    if dealer_upcard == 1:
        dealer_upcard = 11
    total = sum(values)
    aces = values.count(1)
    soft = (aces > 0 and total + 10 <= 21)
    value = total + 10 if soft else total

    if soft:
        if value in [13, 14]:
            return dealer_upcard in [5, 6]
        elif value in [15, 16]:
            return 4 <= dealer_upcard <= 6
        elif value == 17:
            return 3 <= dealer_upcard <= 6
        elif value == 18:
            return 2 <= dealer_upcard <= 6
        elif value == 19:
            return dealer_upcard == 6
        else:
            return False
    else:
        if value == 9:
            return 3 <= dealer_upcard <= 6
        elif value == 10:
            return 2 <= dealer_upcard <= 9
        elif value == 11:
            return True
        else:
            return False

