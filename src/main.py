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
