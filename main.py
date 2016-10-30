#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, \
    QMainWindow, QAction, qApp, QHBoxLayout, QLabel, QLineEdit, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

from SettingsDialog import SettingsDialog
from Settings import Settings
from QuestionGenerator import QuestionGenerator


class Communicate(QObject):
    closeApp = pyqtSignal()


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = Settings()
        self.questions = None
        self.started = False

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        settingsAction = QAction(QIcon('settings.png'), '&Settings', self)
        settingsAction.setShortcut('Ctrl+,')
        settingsAction.setStatusTip('Change settings')
        settingsAction.triggered.connect(self.settings)

        self.startAction = QAction(QIcon('start.png'), '&Start', self)
        self.startAction.setShortcut(Qt.Key_Enter)
        self.startAction.setStatusTip('Start')
        self.startAction.triggered.connect(self.start)

        stopAction = QAction(QIcon('stop.png'), 'Stop', self)
        stopAction.setStatusTip('Stop')
        stopAction.triggered.connect(self.stop)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(settingsAction)
        toolbar.addAction(self.startAction)
        toolbar.addAction(stopAction)

        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.statusBar().showMessage('Ready')
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Fun Math')
        self.show()

    def stop(self):
        self.showResult()
        self.questions = None

    def getCurrAnswer(self):
        t = self.answerEdit.text()
        if t.strip().isnumeric():
            return int(t.strip())
        return -1

    def showQuestion(self, question):
        if question:
            q = question[0]
            a = question[1]
            grid = QHBoxLayout()
            for e in q:
                grid.addWidget(QLabel(str(e)))
            grid.addWidget(QLabel('='))
            self.answerEdit = QLineEdit()
            if a != -1:
                self.answerEdit.setText(str(a))
            grid.addWidget(self.answerEdit)
            mainWidget = QWidget()
            mainWidget.setLayout(grid)
            self.setCentralWidget(mainWidget)
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Do you want to submit?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.showResult()

    def showResult(self):
        pass

    def hideQuestion(self):
        self.setLayout(QHBoxLayout())

    def start(self):
        if not self.questions:
            self.questions = QuestionGenerator(self.settings)
        if not self.started:
            self.showQuestion(self.questions.curr())
            self.started = True
            self.startAction.setIcon(QIcon('pause.png'))
        else:
            self.started = False
            self.hideQuestion()
            self.startAction.setIcon(QIcon('start.png'))

    def settings(self):
        settingGui = SettingsDialog(self, self.settings)
        settingGui.exec_()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Left:
            self.showQuestion(self.questions.previous(self.getCurrAnswer()))
        elif e.key() == Qt.Key_Right:
            self.showQuestion(self.questions.next(self.getCurrAnswer()))

    def mousePressEvent(self, event):
        self.c.closeApp.emit()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
