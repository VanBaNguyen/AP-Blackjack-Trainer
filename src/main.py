import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QHBoxLayout,
    QVBoxLayout, QWidget, QMessageBox, QSpinBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

from blackjack import BlackjackGame, hand_value

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

CARD_PATH = os.path.join(PROJECT_ROOT, "assets", "svg-cards")


def code_to_filename(card_code):
    rank_map = {
        'A': 'ace',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        'T': '10',
        'J': 'jack',
        'Q': 'queen',
        'K': 'king',
    }
    suit_map = {
        'C': 'clubs',
        'D': 'diamonds',
        'H': 'hearts',
        'S': 'spades',
    }
    rank = rank_map[card_code[0]]
    suit = suit_map[card_code[1]]
    return f"{rank}_of_{suit}.svg"

def svg_to_pixmap(svg_path, width=70, height=105):
    if not os.path.exists(svg_path):
        # Fallback: transparent pixmap
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        return QPixmap.fromImage(image)
    renderer = QSvgRenderer(svg_path)
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)
    painter = QPixmap(image)
    painter = QPixmap(width, height)
    painter.fill(Qt.transparent)
    svg_renderer = QSvgRenderer(svg_path)
    painter_obj = QPainter(painter)
    svg_renderer.render(painter_obj)
    painter_obj.end()
    return painter

def get_card_pixmap(card_code):
    filename = code_to_filename(card_code)
    path = os.path.join(CARD_PATH, filename)
    return svg_to_pixmap(path, 70, 105)

def get_card_back_pixmap():
    path = os.path.join(CARD_PATH, "back.svg")
    return svg_to_pixmap(path, 70, 105)

class BlackjackWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casino Blackjack Simulator")
        self.resize(700, 850)
        self.game = BlackjackGame()
        self.init_ui()
        self.update_ui()

    def init_ui(self):
        # Balance and shoe
        self.balance_label = QLabel()
        self.cards_left_label = QLabel()

        top_box = QHBoxLayout()
        top_box.addWidget(self.balance_label)
        top_box.addSpacing(20)
        top_box.addWidget(self.cards_left_label)
        top_box.addStretch(1)

        # Dealer
        self.dealer_label = QLabel("Dealer:")
        self.dealer_cards = QHBoxLayout()
        self.dealer_value_label = QLabel()
        dealer_box = QVBoxLayout()
        dealer_box.addWidget(self.dealer_label)
        dealer_box.addLayout(self.dealer_cards)
        dealer_box.addWidget(self.dealer_value_label)

        # Player
        self.player_label = QLabel("Your Hand(s):")
        self.player_hands_layout = QVBoxLayout()
        player_box = QVBoxLayout()
        player_box.addWidget(self.player_label)
        player_box.addLayout(self.player_hands_layout)
        # Player value labels created dynamically in update_ui

        # Bet controls
        self.bet_input = QSpinBox()
        self.bet_input.setRange(self.game.min_bet, self.game.max_bet)
        self.bet_input.setValue(self.game.min_bet)
        self.bet_button = QPushButton("Place Bet & Deal")
        self.bet_button.clicked.connect(self.place_bet)

        bet_box = QHBoxLayout()
        bet_box.addWidget(QLabel("Bet:"))
        bet_box.addWidget(self.bet_input)
        bet_box.addWidget(self.bet_button)

        # Action buttons
        self.hit_button = QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        self.stand_button = QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        self.double_button = QPushButton("Double")
        self.double_button.clicked.connect(self.double)
        self.split_button = QPushButton("Split")
        self.split_button.clicked.connect(self.split)

        action_box = QHBoxLayout()
        action_box.addWidget(self.hit_button)
        action_box.addWidget(self.stand_button)
        action_box.addWidget(self.double_button)
        action_box.addWidget(self.split_button)

        # Message
        self.message_label = QLabel()

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_box)
        main_layout.addLayout(dealer_box)
        main_layout.addLayout(player_box)
        main_layout.addLayout(bet_box)
        main_layout.addLayout(action_box)
        main_layout.addWidget(self.message_label)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def update_ui(self):
        # Balance and shoe
        self.balance_label.setText(f"Balance: ${self.game.balance}")
        self.cards_left_label.setText(f"Cards Remaining: {self.game.shoe.cards_left()}")

        # Dealer cards
        # Clear dealer card layout completely (widgets and stretches)
        for i in reversed(range(self.dealer_cards.count())):
            item = self.dealer_cards.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.dealer_cards.removeItem(item)

        dealer_hand = self.game.dealer_hand
        for idx, card in enumerate(dealer_hand):
            lbl = QLabel()
            if idx == 1 and self.game.in_progress:
                lbl.setPixmap(get_card_back_pixmap())
            else:
                lbl.setPixmap(get_card_pixmap(card))
            self.dealer_cards.addWidget(lbl, alignment=Qt.AlignLeft)
        self.dealer_cards.addStretch(1)

        # Dealer hand value
        if not dealer_hand:
            self.dealer_value_label.setText("")
        else:
            if self.game.in_progress:
                visible = dealer_hand[:1]
                val, _ = hand_value(visible)
                self.dealer_value_label.setText(f"Dealer shows: {val}")
            else:
                val, _ = hand_value(dealer_hand)
                self.dealer_value_label.setText(f"Dealer: {val}")

        self.clear_layout(self.player_hands_layout)
        self.player_value_labels = []

        # Show each hand with value
        for idx, hand in enumerate(self.game.player_hands):
            hbox = QHBoxLayout()
            for card in hand.cards:
                lbl = QLabel()
                lbl.setPixmap(get_card_pixmap(card))
                hbox.addWidget(lbl)
            hbox.addStretch(1)
            vbox = QVBoxLayout()
            # Hand label
            if len(self.game.player_hands) > 1:
                label = QLabel(f"Hand {idx + 1} (Bet: ${hand.bet})" + (" (Active)" if idx == self.game.current_hand_index else ""))
            else:
                label = QLabel(f"Your Hand (Bet: ${hand.bet})")
            vbox.addWidget(label)
            # Hand value label
            val = hand.value()
            soft = hand.is_soft()
            handtype = "soft" if soft else "hard"
            val_label = QLabel(f"Value: {val} ({handtype})")
            vbox.addWidget(val_label)
            self.player_value_labels.append(val_label)
            vbox.addLayout(hbox)
            self.player_hands_layout.addLayout(vbox)

        # Enable/disable controls
        if not self.game.in_progress:
            self.bet_button.setEnabled(True)
            self.bet_input.setEnabled(True)
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.double_button.setEnabled(False)
            self.split_button.setEnabled(False)
        else:
            self.bet_button.setEnabled(False)
            self.bet_input.setEnabled(False)
            hand = self.game.get_current_hand()
            self.hit_button.setEnabled(not hand.finished)
            self.stand_button.setEnabled(not hand.finished)
            self.double_button.setEnabled(hand.can_double() and not hand.finished and self.game.balance >= hand.bet)
            self.split_button.setEnabled(hand.can_split() and not hand.finished and self.game.balance >= hand.bet)
        self.message_label.setText(self.game.message)

    def place_bet(self):
        bet = self.bet_input.value()
        if self.game.start_round(bet):
            self.update_ui()
        else:
            QMessageBox.warning(self, "Invalid Bet", self.game.message)

    def hit(self):
        self.game.player_hit()
        self.check_hand_end()

    def stand(self):
        self.game.player_stand()
        self.check_hand_end()

    def double(self):
        self.game.player_double()
        self.check_hand_end()

    def split(self):
        self.game.player_split()
        self.update_ui()

    def check_hand_end(self):
        hand = self.game.get_current_hand()
        if hand.finished:
            self.game.advance_hand()
            if self.game.all_player_hands_finished():
                # Dealer plays
                self.game.play_dealer()
                results = self.game.settle_bets()
                # Show all dealer cards
                msg = []
                dealer_val, _ = hand_value(self.game.dealer_hand)
                for idx, (hand, result) in enumerate(zip(self.game.player_hands, results)):
                    val = hand.value()
                    payout, busted = result  # Unpack the tuple
                    if busted:
                        res_text = f"Lose ${hand.bet} (Bust)"
                    elif payout > hand.bet:
                        res_text = f"Win ${payout - hand.bet}"
                    elif payout == hand.bet:
                        res_text = "Push"
                    else:
                        res_text = f"Lose ${hand.bet}"
                    msg.append(f"Hand {idx+1 if len(self.game.player_hands) > 1 else ''}: {val} vs Dealer {dealer_val} → {res_text}")
                self.game.message = "\n".join(msg)
                self.update_ui()
                return
            else:
                self.update_ui()
        else:
            self.update_ui()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackWindow()
    window.show()
    sys.exit(app.exec_())