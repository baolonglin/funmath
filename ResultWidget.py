from PyQt5.QtWidgets import QWidget, QTableView, QSizePolicy, QVBoxLayout, QLabel
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QStandardItem, QFont

class ResultWidget(QWidget):
    def __init__(self, parent, questions):
        super().__init__(parent)
        self.questions = questions

        self.initUI()

    def getScoreWidget(self, score):
        label = QLabel()
        label.setText(self.tr('Score: ') + str(score))
        label.setFont(QFont("Times", 30, QFont.Bold))
        color = 'red'
        if score > 60:
            color = 'green'
        label.setStyleSheet("QLabel { color : " + color + "; }")
        return label

    def initUI(self):
        tableView = QTableView(self)
        report = self.questions.genReport()
        model = QStandardItemModel()
        model.setColumnCount(3)
        model.setRowCount(len(report))
        model.setHorizontalHeaderLabels([self.tr('Question'), self.tr('Your answer'), self.tr('Correct answer')])
        score = 0
        for idx in range(len(report)):
            (question, answer, correctAnswer) = report[idx]
            model.setItem(idx, 0, QStandardItem(question))
            model.setItem(idx, 1, QStandardItem(answer))
            model.setItem(idx, 2, QStandardItem(correctAnswer))
            if answer == correctAnswer:
                model.item(idx, 1).setBackground(QBrush(QColor(0, 255, 0)))
                score += 1
            else:
                model.item(idx, 1).setBackground(QBrush(QColor(255, 0, 0)))
        tableView.setModel(model)

        layout = QVBoxLayout()
        layout.addWidget(self.getScoreWidget(int(score * 100 / len(report))))
        layout.addWidget(tableView)
        self.setLayout(layout)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

