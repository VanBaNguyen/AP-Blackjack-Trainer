import random

class Shoe:
    def __init__(self, num_decks=6, reshuffle_pct=0.8):
        self.num_decks = num_decks
        self.reshuffle_pct = reshuffle_pct
        self.cards = []
        self.discards = []
        self.reshuffle()

    def reshuffle(self):
        """Shuffle all cards back into the shoe."""
        self.cards = [rank + suit
                      for rank in 'A23456789TJQK'
                      for suit in 'HDCS'
                      for _ in range(self.num_decks)]
        random.shuffle(self.cards)
        self.discards = []

    def deal(self):
        """Deal one card. If shoe is low, reshuffle."""
        if len(self.cards) < (1 - self.reshuffle_pct) * self.num_decks * 52:
            self.reshuffle()
        card = self.cards.pop()
        self.discards.append(card)
        return card

    def cards_left(self):
        return len(self.cards)

    def needs_reshuffle(self):
        return len(self.cards) < (1 - self.reshuffle_pct) * self.num_decks * 52
