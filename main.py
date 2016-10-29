#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, \
    QMainWindow, QAction, qApp
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

from SettingsDialog import SettingsDialog
from Settings import Settings


class Communicate(QObject):
    closeApp = pyqtSignal()


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = Settings()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        settingsAction = QAction(QIcon('settings.png'), '&Settings', self)
        settingsAction.setShortcut('Ctrl+,')
        settingsAction.setStatusTip('Change settings')
        settingsAction.triggered.connect(self.settings)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(settingsAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(settingsAction)

        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.statusBar().showMessage('Ready')
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Fun Math')
        self.show()

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
