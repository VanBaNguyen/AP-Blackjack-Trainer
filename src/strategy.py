# strategy.py

def should_split(pair_value, dealer_upcard):
    """pair_value: int (2-10, or 1 for Aces)
       dealer_upcard: int (1 for Ace, 2-10, 11 for Ace)"""
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
    """hand: list of ints (Ace=1, 2-10)
       dealer_upcard: int (1 for Ace, 2-10, 11 for Ace)"""
    if dealer_upcard == 1:
        dealer_upcard = 11
    total = sum(hand)
    aces = hand.count(1)
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
