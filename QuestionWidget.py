from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QFont

class QuestionWidget(QWidget):
    def __init__(self, parent, question):
        super().__init__(parent)
        self.question = question

        self.initUI()

    def getNumWidget(self, n):
        label = QLabel(str(n))
        font = QFont("Times", 14, QFont.Bold)
        label.setFont(font)
        return label

    def getInputWidget(self, n):
        self.answerEdit = QLineEdit()
        if n != -1:
            self.answerEdit.setText(str(n))
        font = QFont("Times", 14, QFont.Bold)
        self.answerEdit.setFont(font)
        self.setFocusProxy(self.answerEdit)
        return self.answerEdit

    def initUI(self):
        q = self.question[0]
        a = self.question[1]
        grid = QHBoxLayout()
        for e in q:
            grid.addWidget(self.getNumWidget(e))
        grid.addWidget(QLabel('='))
        grid.addWidget(self.getInputWidget(a))
        self.setLayout(grid)

    def getAnswer(self):
        t = self.answerEdit.text()
        if t.strip().isnumeric():
            return int(t.strip())
        return -1

