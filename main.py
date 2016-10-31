#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, \
    QMainWindow, QAction, qApp, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

from SettingsDialog import SettingsDialog
from Settings import Settings
from QuestionGenerator import QuestionGenerator
from QuestionWidget import QuestionWidget


class Communicate(QObject):
    closeApp = pyqtSignal()


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = Settings()
        self.questions = None
        self.started = False
        self.questionWidget = None

    def initToolbar(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        settingsAction = QAction(QIcon('settings.png'), '&Settings', self)
        settingsAction.setShortcut('Ctrl+,')
        settingsAction.setStatusTip('Change settings')
        settingsAction.triggered.connect(self.settings)

        self.startAction = QAction(QIcon('start.png'), '&Start', self)
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

    def initUI(self):

        self.initToolbar()

        self.c = Communicate()
        #self.c.closeApp.connect(self.close)

        self.statusBar().showMessage('Ready')
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Fun Math')
        self.show()

    def stop(self):
        if self.started:
            self.start()
        self.showResult()
        self.questions = None

    def showQuestion(self, question):
        if question:
            self.questionWidget = QuestionWidget(self, question)
            layout = QVBoxLayout()
            layout.addStretch(1)
            layout.addWidget(self.questionWidget)
            layout.addStretch(1)
            cmdLayout = QHBoxLayout()
            prevButton = QPushButton("<<")
            prevButton.clicked.connect(self.prevButtonClicked)
            prevButton.setFocusPolicy(Qt.NoFocus)
            nextButton = QPushButton(">>")
            nextButton.clicked.connect(self.nextButtonClicked)
            nextButton.setFocusPolicy(Qt.NoFocus)
            cmdLayout.addWidget(prevButton)
            cmdLayout.addStretch(1)
            cmdLayout.addWidget(nextButton)
            layout.addLayout(cmdLayout)
            centralWidget = QWidget()
            centralWidget.setLayout(layout)
            self.setCentralWidget(centralWidget)
            self.questionWidget.setFocus()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "Do you want to submit?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.showResult()

    def prevButtonClicked(self):
        self.showQuestion(self.questions.previous(self.questionWidget.getAnswer()))

    def nextButtonClicked(self):
        self.showQuestion(self.questions.next(self.questionWidget.getAnswer()))

    def showResult(self):
        pass

    def hideQuestion(self):
        if self.questionWidget:
            self.questions.updateCurrentQuestionAnswer(self.questionWidget.getAnswer())
            self.questionWidget = None
        self.setCentralWidget(QWidget())

    def start(self):
        if not self.questions:
            self.questions = QuestionGenerator(self.settings)
        if not self.started:
            self.showQuestion(self.questions.curr())
            self.started = True
            self.startAction.setIcon(QIcon('pause.png'))
            self.startAction.setStatusTip('Pause')
        else:
            self.started = False
            self.hideQuestion()
            self.startAction.setIcon(QIcon('start.png'))
            self.startAction.setStatusTip('Start')

    def settings(self):
        settingGui = SettingsDialog(self, self.settings)
        settingGui.exec_()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

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
