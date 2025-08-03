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
        self.busted = False
        self.sit_out_mode = False

    def can_split(self):
        return (
            len(self.cards) == 2 and
            card_value(self.cards[0]) == card_value(self.cards[1])
        )

    def can_double(self):
        return len(self.cards) == 2 and not self.doubled

    def add_card(self, card):
        self.cards.append(card)
        if self.is_bust():
            self.finished = True

    def is_bust(self):
        return hand_value(self.cards)[0] > 21

    def is_blackjack(self):
        return is_blackjack(self.cards)

    def value(self):
        return hand_value(self.cards)[0]

    def is_soft(self):
        return hand_value(self.cards)[1]

class BlackjackGame:
    def __init__(self, starting_balance=1000, min_bet=10, max_bet=1000):
        self.shoe = Shoe()
        self.balance = starting_balance
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.reset_round()

    def reset_round(self):
        self.player_hands = []
        self.dealer_hand = []
        self.current_hand_index = 0
        self.current_bet = self.min_bet
        self.in_progress = False
        self.message = ""
        self.sit_out_mode = False

    def start_round(self, bet):
        if bet < self.min_bet or bet > self.max_bet or bet > self.balance:
            self.message = f"Invalid bet: {bet}"
            return False

        self.current_bet = bet
        # Deduct bet *immediately* visual purposes
        self.balance -= bet
        self.player_hands = [PlayerHand(bet)]
        self.dealer_hand = [self.shoe.deal(), self.shoe.deal()]
        for hand in self.player_hands:
            hand.cards = [self.shoe.deal(), self.shoe.deal()]
        self.current_hand_index = 0
        self.in_progress = True
        self.message = ""

        # bj check
        player_bj = self.player_hands[0].is_blackjack()
        dealer_bj = is_blackjack(self.dealer_hand)
        if player_bj:
            self.player_hands[0].finished = True
            if dealer_bj:
                result = self.current_bet     # <--- Add back bet (push)
                self.message = "Push! Both player and dealer have Blackjack."
            else:
                result = int(self.current_bet * 2.5)  # <--- 1.5x win + original bet
                self.message = "Blackjack! You win 1.5x your bet."
            self.balance += result
            self.in_progress = False
            return True

        return True

    def get_current_hand(self):
        return self.player_hands[self.current_hand_index]

    def player_hit(self):
        hand = self.get_current_hand()
        if not hand.finished:
            hand.add_card(self.shoe.deal())
            if hand.is_bust():
                hand.finished = True
                hand.busted = True
            elif hand.value() == 21:
                hand.finished = True

    def player_stand(self):
        hand = self.get_current_hand()
        hand.finished = True

    def player_double(self):
        hand = self.get_current_hand()
        if hand.can_double() and self.balance >= hand.bet:
            self.balance -= hand.bet
            hand.bet *= 2
            hand.doubled = True
            hand.add_card(self.shoe.deal())
            hand.finished = True

    def player_split(self):
        if len(self.player_hands) >= 4:
            self.message = "Maximum number of splits reached (4 hands)."
            return

        hand = self.get_current_hand()
        if hand.can_split() and self.balance >= hand.bet:
            self.balance -= hand.bet
            card1, card2 = hand.cards
            # Replace current hand with two new hands
            self.player_hands[self.current_hand_index] = PlayerHand(hand.bet, [card1, self.shoe.deal()])
            self.player_hands.insert(self.current_hand_index + 1, PlayerHand(hand.bet, [card2, self.shoe.deal()]))

    def advance_hand(self):
        # Move to the next unfinished hand, if any
        while self.current_hand_index < len(self.player_hands) and self.player_hands[self.current_hand_index].finished:
            self.current_hand_index += 1

    def all_player_hands_finished(self):
        return all(h.finished for h in self.player_hands)

    def play_dealer(self):
        """Dealer plays out their hand per standard rules."""
        while True:
            value, is_soft = hand_value(self.dealer_hand)
            if value < 17 or (value == 17 and is_soft):
                self.dealer_hand.append(self.shoe.deal())
            else:
                break

    def settle_bets(self):
        dealer_val, _ = hand_value(self.dealer_hand)
        dealer_bj = is_blackjack(self.dealer_hand)
        results = []
        for hand in self.player_hands:
            if hand.is_bust():
                results.append((0, True)) # Tuple (payout, busted)
                continue
            player_val = hand.value()
            player_bj = hand.is_blackjack()
            if dealer_val > 21:
                result = hand.bet * 2         # <--- Win: give back bet + winnings
            elif player_bj and not dealer_bj:
                result = int(hand.bet * 2.5)  # <--- 1.5x win + original bet
            elif dealer_bj and not player_bj:
                result = 0                    # <--- Player lost
            elif player_val > dealer_val:
                result = hand.bet * 2         # <--- Win: give back bet + winnings
            # Loss
            elif player_val < dealer_val:
                result = 0    
            #Push: give back bet
            else:
                result = hand.bet
            self.balance += result
            results.append((result, False))
        self.in_progress = False
        return results
    
    def sit_out_round(self):
        if self.in_progress:
            self.message = "A round is already in progress."
            return False
        self.sit_out_mode = True
        # No bet, just deal cards
        self.player_hands = [PlayerHand(0)]
        self.dealer_hand = [self.shoe.deal(), self.shoe.deal()]
        for hand in self.player_hands:
            hand.cards = [self.shoe.deal(), self.shoe.deal()]
            hand.finished = True  # Don't play out, player is sitting out
        self.current_hand_index = 0
        self.in_progress = True
        self.message = "Sit Out: Hand dealt. No action taken."
        return True

    def sit_out_settle(self):
        # Just end the round. No money is affected, but mark as done.
        self.in_progress = False
        self.message = "Sit Out: Hand played, no bet placed."

