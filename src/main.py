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
