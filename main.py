#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDesktopWidget, \
    QMainWindow, QAction, qApp, QLabel, QCheckBox, QLineEdit, QGridLayout, \
    QDialog, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSettings
from PyQt5.QtGui import QIcon


class Communicate(QObject):
    closeApp = pyqtSignal()


class Settings(QDialog):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.initUI()

    def initUI(self):
        minLabel = QLabel('Min Number')
        maxLabel = QLabel('Max Number')
        supportOp = QLabel('Supported Operation')

        self.minEdit = QLineEdit(str(self.settings.value('min', 0)), self)
        self.maxEdit = QLineEdit(str(self.settings.value('max', 100)), self)
        
        self.cbAdd = QCheckBox('+')
        self.cbAdd.setChecked(self.settings.value('op_plus', True))
        self.cbMinus = QCheckBox('-')
        self.cbMinus.setChecked(self.settings.value('op_minus', True))
        self.cbMulti = QCheckBox('*')
        self.cbMulti.setChecked(self.settings.value('op_multi', False))
        self.cbDivid = QCheckBox('/')
        self.cbDivid.setChecked(self.settings.value('op_divid', False))

        gridOp = QHBoxLayout()
        gridOp.addWidget(self.cbAdd)
        gridOp.addWidget(self.cbMinus)
        gridOp.addWidget(self.cbMulti)
        gridOp.addWidget(self.cbDivid)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(minLabel, 1, 0)
        grid.addWidget(self.minEdit, 1, 1)
        grid.addWidget(maxLabel, 1, 2)
        grid.addWidget(self.maxEdit, 1, 3)
        grid.addWidget(supportOp, 2, 0)
        grid.addLayout(gridOp, 2, 1, 1, 3)
        self.setLayout(grid)

        self.setWindowTitle('Settings')
        self.resize(500, 300)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, e):
        self.settings.setValue('min', int(self.minEdit.text()))
        self.settings.setValue('max', int(self.maxEdit.text()))

        self.settings.setValue('op_plus', self.cbAdd.isChecked())
        self.settings.setValue('op_minus', self.cbMinus.isChecked())
        self.settings.setValue('op_multi', self.cbMulti.isChecked())
        self.settings.setValue('op_divid', self.cbDivid.isChecked())

        super().closeEvent(e)


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSettings()

    def initSettings(self):
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

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
        settingGui = Settings(self, self.settings)
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
