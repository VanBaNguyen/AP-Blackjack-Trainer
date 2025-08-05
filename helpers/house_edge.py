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
    
    def initUI(self):
        layout = QVBoxLayout()
        
        header = QLabel("House Edge Calculator")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Options Grid
        grid = QGridLayout()
        
        # H17
        h17_box = self.make_option_group("Does the Dealer Hit or Stand on Soft 17?", ["Hits", "Stands"], "H17")
        grid.addWidget(h17_box, 0, 0)
        
        # DAS
        das_box = self.make_option_group("Can the Player Double After Splitting?", ["Yes", "No"], "DAS")
        grid.addWidget(das_box, 1, 0)
        
        # DOUBLE
        double_box = self.make_option_group("When Can a Player Double?", ["Any First Two Cards", "9-11 Only", "10-11 Only"], "DOUBLE")
        grid.addWidget(double_box, 2, 0)
        
        # RSA
        rsa_box = self.make_option_group("Can Player Split Aces More Than Once?", ["Yes", "No"], "RSA")
        grid.addWidget(rsa_box, 3, 0)
        
        # LS
        ls_box = self.make_option_group("Is Late surrender allowed?", ["Yes", "No"], "LS")
        grid.addWidget(ls_box, 4, 0)
        
        layout.addLayout(grid)
        
        # House Edge Table
        self.edge_labels = {}
        table = QHBoxLayout()
        decks = [1, 2, 4, 6, 8]
        self.deck_keys = decks
        deck_names = ["Single Deck", "Double Deck", "4 Decks", "6 Decks", "8 Decks"]
        for name, d in zip(deck_names, decks):
            v = QVBoxLayout()
            title = QLabel(name)
            title.setFont(QFont("Arial", 10, QFont.Bold))
            v.addWidget(title, alignment=Qt.AlignCenter)
            edge_lbl = QLabel("0.000")
            edge_lbl.setFont(QFont("Arial", 16, QFont.Bold))
            v.addWidget(edge_lbl, alignment=Qt.AlignCenter)
            self.edge_labels[d] = edge_lbl
            table.addLayout(v)
        frame = QFrame()
        frame.setLayout(table)
        frame.setStyleSheet("background-color: #21212b; border-radius: 8px;")
        layout.addWidget(frame)
        
        self.setLayout(layout)
        self.resize(700, 500)
        self.update_edges()
    
    def make_option_group(self, title, options, key):
        groupbox = QGroupBox()
        groupbox.setStyleSheet("background-color: #23232f; border-radius: 6px;")
        v = QVBoxLayout()
        label = QLabel(title)
        label.setFont(QFont("Arial", 11, QFont.Bold))
        v.addWidget(label)
        h = QHBoxLayout()
        self.__dict__[f"{key}_group"] = QButtonGroup(self)
        for opt in options:
            radio = QRadioButton(opt)
            radio.setFont(QFont("Arial", 10))
            radio.setStyleSheet("QRadioButton { padding: 4px; }")
            if key == "H17" and opt == "Hits": radio.setChecked(True)
            if key == "DAS" and opt == "Yes": radio.setChecked(True)
            if key == "DOUBLE" and opt == "Any First Two Cards": radio.setChecked(True)
            if key == "RSA" and opt == "No": radio.setChecked(True)
            if key == "LS" and opt == "No": radio.setChecked(True)
            h.addWidget(radio)
            self.__dict__[f"{key}_group"].addButton(radio)
            radio.toggled.connect(self.update_edges)
        v.addLayout(h)
        groupbox.setLayout(v)
        return groupbox

    def get_rule_values(self):
        rules = {
            'H17': self.H17_group.buttons()[0].isChecked(),  # Hits
            'DAS': self.DAS_group.buttons()[0].isChecked(),  # Yes
            'DOUBLE': "Any" if self.DOUBLE_group.buttons()[0].isChecked() else (
                "9-11" if self.DOUBLE_group.buttons()[1].isChecked() else "10-11"
            ),
            'RSA': self.RSA_group.buttons()[0].isChecked(),  # Yes
            'LS': self.LS_group.buttons()[0].isChecked(),    # Yes
        }
        return rules

    def update_edges(self):
        rules = self.get_rule_values()
        for d in self.deck_keys:
            edge = calc_house_edge({
                "H17": rules['H17'],
                "DAS": rules['DAS'],
                "DOUBLE": rules['DOUBLE'],
                "RSA": rules['RSA'],
                "LS": rules['LS'],
            }, d)
            self.edge_labels[d].setText(f"{edge:.3f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HouseEdgeCalculator()
    win.show()
    sys.exit(app.exec_())
