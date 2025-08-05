import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup,
    QGroupBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Rule adjustments per Stanford Wong's chart
def calc_house_edge(rules, decks):
    edge = 0.0
    # Decks
    deck_vals = {1: 0.00, 2: 0.32, 4: 0.47, 6: 0.52, 8: 0.55}
    edge += deck_vals[decks]
    # H17
    if rules['H17']:
        edge += 0.20
    # DAS
    if rules['DAS']:
        edge += -0.14
    # DOUBLE
    if rules['DOUBLE'] == "9-11":
        edge += 0.08
    elif rules['DOUBLE'] == "10-11":
        edge += 0.17
    # RSA
    if rules['RSA']:
        edge += -0.08
    # LS
    if rules['LS']:
        edge += -0.08
    return round(edge, 3)

class HouseEdgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("House Edge Calculator (lower is better)")
        self.setStyleSheet("background-color: #18171c; color: #fff;")
        self.initUI()
    

