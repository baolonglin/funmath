#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMainWindow
from PyQt5.QtCore import QCoreApplication

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.setToolTip('This is a <b>QPushButton</b> widget')
        qbtn.move(50, 50)

        self.statusBar().showMessage('Ready')
        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Example')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())
    
