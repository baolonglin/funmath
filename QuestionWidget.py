from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QFontMetrics
from QuestionGenerator import Operator

class QuestionWidget(QWidget):
    def __init__(self, parent, question):
        super().__init__(parent)
        self.question = question

        self.parseQuestion()
        self.initUI()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        f = self.font()
        cr = self.contentsRect()

        dw = event.size().width() - event.oldSize().width()  # width change
        dh = event.size().height() - event.oldSize().height()  # height change
        fs = max(f.pixelSize(), 1)
        while True:
            f.setPixelSize(fs)
            text = self.questionAnswerStr()
            br = QFontMetrics(f).boundingRect(text)  # question and answer string
            if dw >= 0 and dh >= 0:
                if br.height() <= cr.height() and br.width() <= cr.width():
                    fs += 1
                else:
                    f.setPixelSize(max(fs - 1, 1))  # backtrack
                    break
            else:
                if br.height() > cr.height() or br.width() > cr.width():
                    fs -= 1
                else:
                    break

            if fs < 1:
                break
        self.setFont(f)

    def parseQuestion(self):
        questionStrForEval = ''
        self.questionStrShow = ''
        for item in self.question[0]:
            questionStrForEval += str(item)
            if item in Operator:
                self.questionStrShow += self.opEnumToStr(item)
            else:
                self.questionStrShow += str(item)
        self.correctAnswer = eval(questionStrForEval)

    def questionAnswerStr(self):
        return self.questionStrShow + self.tr('=') + str(self.correctAnswer)

    def opEnumToStr(self, op):
        if op.value == 1:
            return self.tr("+")
        elif op.value == 2:
            return self.tr('-')
        elif op.value == 3:
            return self.tr('*')
        elif op.valuse == 4:
            return self.tr('/')

    def getNumWidget(self, text):
        label = QLabel(text)
        label.setFont(self.font())
        return label

    def getInputWidget(self, n):
        self.answerEdit = QLineEdit()
        self.answerEdit.setInputMask('#' * len(str(self.correctAnswer)))
        if n != -1:
            self.answerEdit.setText(str(n))
        self.answerEdit.setFont(self.font())
        self.setFocusProxy(self.answerEdit)
        return self.answerEdit

    def initUI(self):
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))

        q = self.question[0]
        a = self.question[1]
        grid = QHBoxLayout()

        qstr = ""
        for e in q:
            if e in Operator:
                qstr += self.opEnumToStr(e)
            else:
                qstr += str(e)
        qstr += self.tr('=')
        grid.addWidget(self.getNumWidget(qstr))
        grid.addWidget(self.getInputWidget(a))
        self.setLayout(grid)

    def getAnswer(self):
        t = self.answerEdit.text()
        if t.strip().isnumeric():
            return int(t.strip())
        return -1

