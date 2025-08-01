import random

class Shoe:
    def __init__(self, num_decks=6, reshuffle_pct=0.8):
        self.num_decks = num_decks
        self.reshuffle_pct = reshuffle_pct
        self.cards = []
        self.discards = []
        self.running_count = 0
        self.reshuffle()

    def reshuffle(self):
        """Shuffle all cards back into the shoe."""
        self.cards = [rank + suit
                      for rank in 'A23456789TJQK'
                      for suit in 'HDCS'
                      for _ in range(self.num_decks)]
        random.shuffle(self.cards)
        self.discards = []
        self.running_count = 0
    
    def count_card(self, card):
        """Update the running count based on the card dealt."""
        rank = card[0]
        # Hi-Lo system
        if rank in '23456':
            self.running_count += 1
        elif rank in 'TJQKA':
            self.running_count -= 1
        # 7,8,9 = 0

    def deal(self):
        """Deal one card. If shoe is low, reshuffle."""
        if len(self.cards) < (1 - self.reshuffle_pct) * self.num_decks * 52:
            self.reshuffle()
        card = self.cards.pop()
        self.discards.append(card)
        self.count_card(card)
        return card

    def cards_left(self):
        return len(self.cards)

    def needs_reshuffle(self):
        return len(self.cards) < (1 - self.reshuffle_pct) * self.num_decks * 52
    
    def get_running_count(self):
        return self.running_count

    def get_true_count(self):
        decks_remaining = len(self.cards) / 52.0
        if decks_remaining == 0:
            return 0
        return self.running_count / decks_remaining
