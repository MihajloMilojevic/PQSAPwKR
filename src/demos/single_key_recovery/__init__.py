from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem, QScrollArea, QFrame, QMessageBox
    
)
import sys
from PyQt5.QtCore import Qt
from ... import key_recovery as kr

class SingleKeyRecoveryDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.shares = []
        self.compontents = []

    def initUI(self):
        
        self.font = self.font()
        self.font.setFamily("Times New Roman")
        self.font.setPointSize(14)
        self.setFont(self.font)

        layout = QVBoxLayout()
        
        # Top input fields
        top_layout = QHBoxLayout()
        self.t_input = QLineEdit()
        self.n_input = QLineEdit()
        self.prime_input = QLineEdit()
        
        top_layout.addWidget(QLabel("t:"))
        top_layout.addWidget(self.t_input)
        top_layout.addWidget(QLabel("n:"))
        top_layout.addWidget(self.n_input)
        top_layout.addWidget(QLabel("prime:"))
        top_layout.addWidget(self.prime_input)
        
        layout.addLayout(top_layout)

        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Gives it a nice look
        
        layout.addWidget(line)

        # Key input
        key_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.generate_button = QPushButton("Generate Shares")
        self.generate_button.setMinimumWidth(250)

        self.generate_button.clicked.connect(self.generate_shares)

        key_layout.addWidget(QLabel("key:"))
        key_layout.addWidget(self.key_input)
        key_layout.addWidget(self.generate_button)
        
        layout.addLayout(key_layout)

        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Gives it a nice look
        
        layout.addWidget(line)

        # Commitment area
        commit_layout = QHBoxLayout()
        commit_layout.addWidget(QLabel("Commitment:"))
        self.commit_input = QLineEdit()
        self.commit_input.setReadOnly(True)
        commit_layout.addWidget(self.commit_input)
        layout.addLayout(commit_layout)

        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Gives it a nice look
        
        layout.addWidget(line)
        
        # Shares area
        shares_layout = QHBoxLayout()
        
        left_layout = QScrollArea()
        left_layout.setWidgetResizable(True)
        left_layout.setWidget(QWidget())
        left_layout.widget().setLayout(QVBoxLayout())

        right_layout = QScrollArea()
        right_layout.setWidgetResizable(True)
        right_layout.setWidget(QWidget())
        right_layout.widget().setLayout(QVBoxLayout())            
        
        shares_layout.addWidget(left_layout)
        shares_layout.addWidget(right_layout)
        layout.addLayout(shares_layout)

        self.left_layout = left_layout
        self.right_layout = right_layout
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Gives it a nice look
        
        layout.addWidget(line)
        
        # Recovery section
        recover_layout = QHBoxLayout()
        self.recover_key_input = QLineEdit()
        self.recover_key_input.setReadOnly(True)
        self.recover_button = QPushButton("Recover")
        self.recover_button.setMinimumWidth(250)
        self.recover_button.clicked.connect(self.recover_key)
        recover_layout.addWidget(QLabel("key:"))
        recover_layout.addWidget(self.recover_key_input)

        self.recovry_valid_label = QLabel("")
        self.recovry_valid_label.setFont(self.font)
        self.recovry_valid_label.setAlignment(Qt.AlignCenter)
        self.recovry_valid_label.setMinimumWidth(100)
        recover_layout.addWidget(self.recovry_valid_label)
        recover_layout.addWidget(self.recover_button)
        
        layout.addLayout(recover_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("Single Key Recovery Demo")
        self.show()

    def get_params(self):
        if not self.t_input.text():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("t is required")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False, None, None, None
        if not self.n_input.text():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("n is required")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False, None, None, None
        t, n, prime = None, None, None
        try:
            t = int(self.t_input.text())
            n = int(self.n_input.text())
            if self.prime_input.text():
                prime = int(self.prime_input.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("t, n and prime must be integers")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False, None, None, None
        
        if t > n:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("t must be less than n")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False, None, None, None
        
        if t < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("t must be greater than 0")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False, None, None, None

        return True, t, n, prime

    def print_shares(self):
        self.right_layout.widget().setVisible(False)
        self.right_layout.widget().deleteLater()
        self.right_layout.setWidget(QWidget())
        self.right_layout.widget().setLayout(QVBoxLayout())
        self.compontents = []
        for i in range(len(self.shares)):
            share = self.shares[i]
            share_box, btn, label, share_input, tag_input = self.generate_right_share_box(i+1, f"{share.share[0]}, {share.share[1]}", share.tag)
            self.right_layout.widget().layout().addLayout(share_box)
            if i != len(self.shares) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                self.right_layout.widget().layout().addWidget(line)
            self.compontents.append((label, share_input, tag_input))
            btn.clicked.connect(self.remove_share(i))
            share_input.textChanged.connect(self.share_changed(i))
            tag_input.textChanged.connect(self.tag_changed(i))
        self.right_layout.widget().layout().addStretch(1)
    
    def tag_changed(self, index):
        def f():
            original_text = self.shares[index].tag
            text = self.compontents[index][2].text().lower()
            self.compontents[index][2].setText(text)
            if not text:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("tag is required")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.compontents[index][2].setText(original_text)
                return
            for c in text:
                if c not in "0123456789abcdef":
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText("tag must be a hex string")
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    self.compontents[index][2].setText(original_text)
                    return    
            self.shares[index].tag = text
        return f
    
    def share_changed(self, index):
        def f():
            share_og = self.shares[index].share
            original_text = f"{share_og[0]}, {share_og[1]}"
            text = self.compontents[index][1].text().lower()
            self.compontents[index][1].setText(text)
            if not text:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("share is required")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.compontents[index][1].setText(original_text)
                return
            if "," not in text or text.count(",") > 1:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("share must be two hex numbers separated by a comma")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.compontents[index][1].setText(original_text)
                return
            text = text.replace(" ", "")
            share = tuple(text.split(","))
            for s in share:
                for c in s:
                    if c not in "0123456789abcdef":
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Icon.Critical)
                        msg.setText("share must be a hex string")
                        msg.setWindowTitle("Error")
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        self.compontents[index][1].setText(original_text)
                        return
            self.shares[index].share = share
        return f

    def remove_share(self, index):
        def f():
            self.shares.pop(index)
            self.print_shares()
        return f

    def transfer_share(self, share):
        def f():
            self.shares.append(share)
            self.print_shares()
        return f

    def generate_shares(self):
        params_ok, t, n, prime = self.get_params()
        if not params_ok:
            return
        key = self.key_input.text()
        if not key:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("key is required")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        try:
            key = int(key)
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("key must be an integer")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        generator = kr.single_key.SingleKeyGenerator(t, prime)
        generator.commit(key)
        self.commit_input.setText(kr.utils.to_hex_no_prefix(generator.commitment))
        shares = generator.generate_shares("password", n)
        for i in reversed(range(self.left_layout.widget().layout().count())): 
            widget = self.left_layout.widget().layout().itemAt(i).widget()
            if not widget:
                continue
            self.left_layout.widget().layout().removeWidget(widget)
            widget.setParent(None)
        self.left_layout.widget().setVisible(False)
        self.left_layout.widget().deleteLater()
        self.left_layout.setWidget(QWidget())
        self.left_layout.widget().setLayout(QVBoxLayout())
        for i in range(len(shares)):
            share = shares[i]
            share_box, btn = self.generate_left_share_box(i+1, f"{share.share[0]}, {share.share[1]}", share.tag)
            self.left_layout.widget().layout().addLayout(share_box)
            if i != len(shares) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)  # Horizontal line
                line.setFrameShadow(QFrame.Sunken)  # Gives it a nice look
                self.left_layout.widget().layout().addWidget(line)

            btn.clicked.connect(self.transfer_share(share))
        
        self.left_layout.widget().layout().addStretch(1)
        self.shares = []
        self.right_layout.widget().setVisible(False)
        self.right_layout.widget().deleteLater()
        self.right_layout.setWidget(QWidget())
        self.right_layout.widget().setLayout(QVBoxLayout())

    def generate_left_share_box(self, index, share, tag):
        box_layout = QHBoxLayout()
        inputs_layout = QVBoxLayout()
        share_layout = QHBoxLayout()
        share_layout.addWidget(QLabel(f"S {index}: "))
        share_input = QLineEdit(share)
        share_input.setReadOnly(True)
        share_layout.addWidget(share_input)
        inputs_layout.addLayout(share_layout)
        tag_layout = QHBoxLayout()
        tag_layout.addWidget(QLabel(f"T {index}:"))
        tag_input = QLineEdit(tag)
        tag_input.setReadOnly(True)
        tag_layout.addWidget(tag_input)
        inputs_layout.addLayout(tag_layout)
        box_layout.addLayout(inputs_layout)
        btn = QPushButton(">>")
        btn.setFixedWidth(50)
        box_layout.addWidget(btn)
        return box_layout, btn
        
    def generate_right_share_box(self, index, share, tag):
        box_layout = QHBoxLayout()
        btn = QPushButton("X")
        btn.setFixedWidth(50)
        box_layout.addWidget(btn)
        inputs_layout = QVBoxLayout()
        share_layout = QHBoxLayout()
        share_layout.addWidget(QLabel(f"S {index}:"))
        share_input = QLineEdit(share)
        share_layout.addWidget(share_input)
        inputs_layout.addLayout(share_layout)
        tag_layout = QHBoxLayout()
        tag_layout.addWidget(QLabel(f"T {index}:"))
        tag_input = QLineEdit(tag)
        tag_layout.addWidget(tag_input)
        inputs_layout.addLayout(tag_layout)
        box_layout.addLayout(inputs_layout)
        label = QLabel("")
        label.setMinimumWidth(100)
        box_layout.addWidget(label)
        return box_layout, btn, label, share_input, tag_input

    def validate_shares(self):
        validator = kr.single_key.SingleKeyValidator(kr.utils.from_hex_no_prefix(self.commit_input.text()))
        for i in range(len(self.shares)):
            share = self.shares[i]
            if not validator.validate_share(share, "password"):
                self.compontents[i][0].setText("invalid")
                self.compontents[i][0].setStyleSheet("color: red")
            else:
                self.compontents[i][0].setText("valid")
                self.compontents[i][0].setStyleSheet("color: green")
            self.compontents[i][0].setFont(self.font)
            self.compontents[i][0].setAlignment(Qt.AlignCenter)

    def recover_key(self):
        self.validate_shares()
        params_ok, t, n, prime = self.get_params()
        if not params_ok:
            return
        recoverer = kr.single_key.SingleKeyRecoverer(t, prime)
        try:
            key = recoverer.recover(self.shares)
            self.recover_key_input.setText(str(key))
            validator = kr.single_key.SingleKeyValidator(kr.utils.from_hex_no_prefix(self.commit_input.text()))
            if validator.validate_secret(key):
                self.recovry_valid_label.setText("valid")
                self.recovry_valid_label.setStyleSheet("color: green")
            else:
                self.recovry_valid_label.setText("invalid")
                self.recovry_valid_label.setStyleSheet("color: red")
        except ValueError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(str(e))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

def singleKeyRecoveryDemoRunner():
    app = QApplication(sys.argv)
    demo = SingleKeyRecoveryDemo()
    sys.exit(app.exec_())