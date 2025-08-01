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

def best_move_soft(hand, dealer_upcard):
    """
    hand: list of card codes or ints (Ace=1, 2-10)
    dealer_upcard: int or card code string
    Returns: 'H', 'S', 'D', or 'Ds'
    """
    values = hand_to_int_list(hand)
    if isinstance(dealer_upcard, str):
        dealer_upcard = card_str_to_int(dealer_upcard)
    if dealer_upcard == 1:
        dealer_upcard = 11
    total = sum(values)
    aces = values.count(1)
    soft = (aces > 0 and total + 10 <= 21)
    value = total + 10 if soft else total

    if not soft or value < 13 or value > 20:
        return None

    chart = {
        20: ["S"]*10,                                        # A,9
        19: ["S","S","S","S","Ds","S","S","S","S","S"],     # A,8 (Ds vs 6)
        18: ["Ds","Ds","Ds","Ds","Ds","S","S","H","H","H"], # A,7
        17: ["H","D","D","D","D","H","H","H","H","H"],      # A,6
        16: ["H","H","D","D","D","H","H","H","H","H"],      # A,5
        15: ["H","H","D","D","D","H","H","H","H","H"],      # A,4
        14: ["H","H","H","D","D","H","H","H","H","H"],      # A,3
        13: ["H","H","H","D","D","H","H","H","H","H"],      # A,2
    }

    idx = dealer_upcard - 2 if dealer_upcard != 11 else 9

    move = chart[value][idx]
    return move

def best_move_hard(hand, dealer_upcard):
    """
    Given a blackjack hand (list of ints or card codes) and dealer upcard (int or code),
    return the best move for hard totals according to standard basic strategy.
    Returns:
        'H' - Hit
        'S' - Stand
        'D' - Double if allowed, otherwise hit
    """
    values = hand_to_int_list(hand)
    if isinstance(dealer_upcard, str):
        dealer_upcard = card_str_to_int(dealer_upcard)

    if dealer_upcard == 1:
        dealer_upcard = 11
    total = sum(values)
    # Only apply this for hard hands (not soft hands)
    if 1 in values and total + 10 <= 21:
        return None

    # Hard total strategy chart, based on your image.
    # Rows: player hard total (17-8), Columns: dealer upcard (2-11)
    chart = {
        17: ["S"] * 10,
        16: ["S","S","S","S","S","H","H","H","H","H"],
        15: ["S","S","S","S","S","H","H","H","H","H"],
        14: ["S","S","S","S","S","H","H","H","H","H"],
        13: ["S","S","S","S","S","H","H","H","H","H"],
        12: ["H","H","S","S","S","H","H","H","H","H"],
        11: ["D"] * 10,
        10: ["D","D","D","D","D","D","D","D","H","H"],
        9:  ["H","D","D","D","D","H","H","H","H","H"],
        8:  ["H"] * 10,
    }

    # For totals above 17 or below 8, use standard plays
    if total >= 17:
        return "S"
    if total <= 8:
        return "H"

    # Dealer upcard 2-11 (2-10, 11=Ace)
    idx = dealer_upcard - 2 if dealer_upcard != 11 else 9

    # For totals 9-16, look up in chart
    if total in chart:
        return chart[total][idx]

    # Fallback for any hand not covered (shouldn't happen)
    return None

def check_playing_deviations(hand, dealer_upcard, true_count):
    """
    Given hand, dealer upcard, and true count,
    returns one of ('Stand', 'Hit', 'Double', 'Split') or None if no deviation.
    Pair of 10s is 10, 10 or any face cards that sum to 20.
    """
    values = hand_to_int_list(hand)
    if isinstance(dealer_upcard, str):
        dealer_upcard = card_str_to_int(dealer_upcard)
    total = sum(values)
    is_pair = len(values) == 2 and values[0] == values[1]
    # Check for Pair of 10s even if they're face cards
    pair_of_10s = (
        len(values) == 2 and
        card_str_to_int(hand[0]) == 10 and
        card_str_to_int(hand[1]) == 10
    )
    # ------------- VARIANCE PLAYS -------------
    # Format: (player total or pair, dealer card, required TC, move, sense)
    deviations = [
        # (Player total, Dealer upcard, TC threshold, Action, Direction (">=", "<="))
        (16, 9,   5,  "Stand",  ">="),
        (16, 10,  0,  "Stand",  ">="),
        (15, 10,  4,  "Stand",  ">="),
        (13, 2,  -1,  "Stand",  ">="),
        (13, 3,  -2,  "Stand",  ">="),
        (12, 2,   4,  "Stand",  ">="),
        (12, 3,   2,  "Stand",  ">="),
        (12, 4,   0,  "Stand",  ">="),
        (12, 5,  -1,  "Stand",  ">="),
        (12, 6,  -1,  "Stand",  ">="),
        (11, 11,  1,  "Double", ">="), # 11 vs Ace
        (10, 10,  4,  "Double", ">="),
        (10, 11,  4,  "Double", ">="),
        (9, 2,    1,  "Double", ">="),
        (9, 7,    4,  "Double", ">="),
        # Pair of 10s
        ("pair10", 5,  5, "Split", ">="),
        ("pair10", 6,  5, "Split", ">="),
    ]
    for rule in deviations:
        p_val, d_card, req_tc, move, sense = rule
        if p_val == "pair10":
            if not pair_of_10s:
                continue
            if dealer_upcard != d_card:
                continue
            if (sense == ">=" and true_count >= req_tc) or (sense == "<=" and true_count <= req_tc):
                return move
        else:
            if total != p_val:
                continue
            if dealer_upcard != d_card:
                continue
            if (sense == ">=" and true_count >= req_tc) or (sense == "<=" and true_count <= req_tc):
                return move
    return None
