from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, \
    QHBoxLayout, QGridLayout, QDesktopWidget


class SettingsDialog(QDialog):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self.initUI()

    def initUI(self):
        minLabel = QLabel('Min Number')
        maxLabel = QLabel('Max Number')
        supportOp = QLabel('Supported Operation')
        questionLabel = QLabel('Question Number')
        opNumLebel = QLabel('Operator number')

        self.minEdit = QLineEdit(str(self.settings.getMinNum()), self)
        self.maxEdit = QLineEdit(str(self.settings.getMaxNum()), self)
        self.questionNumberEdit = QLineEdit(
            str(self.settings.getQuestionNum()), self)
        self.opNumberEdit = QLineEdit(
            str(self.settings.getOperatorNum()), self)

        self.cbAdd = QCheckBox('+')
        self.cbAdd.setChecked(self.settings.isPlusEnable())
        self.cbMinus = QCheckBox('-')
        self.cbMinus.setChecked(self.settings.isMinusEnable())
        self.cbMulti = QCheckBox('*')
        self.cbMulti.setChecked(self.settings.isMultiEnable())
        self.cbDivid = QCheckBox('/')
        self.cbDivid.setChecked(self.settings.isDivideEnable())
        self.cbNegative = QCheckBox('Support Negative Result')
        self.cbNegative.setChecked(self.settings.isSupportNegative())

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
        grid.addWidget(questionLabel, 3, 0)
        grid.addWidget(self.questionNumberEdit, 3, 1)
        grid.addWidget(opNumLebel, 3, 2)
        grid.addWidget(self.opNumberEdit, 3, 3)
        grid.addWidget(self.cbNegative, 4, 0, 1, 2)
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
        self.settings.setMinNum(int(self.minEdit.text()))
        self.settings.setMaxNum(int(self.maxEdit.text()))

        self.settings.setPlusEnable(self.cbAdd.isChecked())
        self.settings.setMinusEnable(self.cbMinus.isChecked())
        self.settings.setMultiEnable(self.cbMulti.isChecked())
        self.settings.setDivideEnable(self.cbDivid.isChecked())

        self.settings.setQuestionNum(int(self.questionNumberEdit.text()))
        self.settings.setOperatorNum(int(self.opNumberEdit.text()))

        self.settings.setSupportNegative(self.cbNegative.isChecked())
        super().closeEvent(e)
