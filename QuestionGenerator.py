
from enum import Enum
import random

class Operator(Enum):
    plus = 1
    minus = 2
    multiply = 3
    divide = 4

    def highPriorityThen(self, op2):
        if self in [Operator.plus, Operator.minus]:
            if op2 in [Operator.plus, Operator.minus]:
                return True
            else:
                return False
        else:
            return True

    def __str__(self):
        if self.value == 1:
            return "+"
        elif self.value == 2:
            return '-'
        elif self.value == 3:
            return '*'
        elif self.value == 4:
            return '/'

class QuestionGenerator:

    def __init__(self, settings):
        self.settings = settings
        self.supportedOp = []
        self.generatedQuestions = []
        self.answers = []
        self.current_question_idx = 0

        self.initSupportedOp()
        self.initQuestion()

    def initSupportedOp(self):
        if self.settings.isPlusEnable():
            self.supportedOp.append(Operator.plus)
        if self.settings.isMinusEnable():
            self.supportedOp.append(Operator.minus)
        if self.settings.isMultiEnable():
            self.supportedOp.append(Operator.multiply)
        if self.settings.isDivideEnable():
            self.supportedOp.append(Operator.divide)

    def getRandNum(self):
        return random.randint(self.settings.getMinNum(),
                              self.settings.getMaxNum())
    def getRandOp(self):
        return self.supportedOp[
            random.randint(0, len(self.supportedOp) - 1)]

    def noNegative(self, question):
        parseIntoPostFix = []
        currOp = None
        for item in question:
            if item in Operator:
                if not currOp:
                    currOp = item
                else:
                    if currOp.highPriorityThen(item):
                        parseIntoPostFix.append(currOp)
                        currOp = item
                    else:
                        parseIntoPostFix.append(item)
            else:
                parseIntoPostFix.append(item)
        if currOp:
            parseIntoPostFix.append(currOp)

        exprStack = []
        while len(parseIntoPostFix) > 0:
            item = parseIntoPostFix.pop(0)

            if item in Operator:
                if item is Operator.minus:
                    if len(exprStack) > 1:
                        tmp = exprStack.pop()
                        result = exprStack.pop() - tmp
                        if result < 0:
                            return False
                        exprStack.append(result)
                    else:
                        return False
                elif item is Operator.divide:
                    if len(exprStack) > 1:
                        tmp = exprStack.pop()
                        exprStack.append(exprStack.pop() / tmp)
                else:
                    if len(exprStack) > 1:
                        exprStack.append(eval(str(exprStack.pop()) + str(item) + str(exprStack.pop())))
                    else:
                        return False
            else:
                exprStack.append(item)
        return True

    def isDuplicate(self, question):
        return question in self.generatedQuestions

    def filterQuestion(self, question):
        ret = True
        if not self.settings.isSupportNegative():
            ret = ret and self.noNegative(question)

        ret = ret and not self.isDuplicate(question)
        return ret

    def initQuestion(self):
        for q_idx in range(self.settings.getQuestionNum()):
            while True:
                question = []
                for i_idx in range(self.settings.getOperatorNum()):
                    question.append(self.getRandNum())
                    question.append(self.getRandOp())
                question.append(self.getRandNum())
                if self.filterQuestion(question):
                    self.generatedQuestions.append(question)
                    self.answers.append(-1)
                    break

    def curr(self):
        return self.generatedQuestions[self.current_question_idx], self.answers[self.current_question_idx]

    def updateCurrentQuestionAnswer(self, answer):
        if self.current_question_idx < len(self.generatedQuestions):
            self.answers[self.current_question_idx] = answer

    def previous(self, answer):
        self.updateCurrentQuestionAnswer(answer)
        self.current_question_idx -= 1
        if self.current_question_idx >= 0:
            return self.curr()
        self.current_question_idx += 1
        return None

    def next(self, answer):
        self.updateCurrentQuestionAnswer(answer)
        self.current_question_idx += 1
        if self.current_question_idx < len(self.generatedQuestions):
            return self.curr()
        self.current_question_idx -= 1
        return None

    def genReport(self):
        report = []
        for idx in range(len(self.generatedQuestions)):
            question = ''
            for item in self.generatedQuestions[idx]:
                question += str(item)
            answer = ''
            if self.answers[idx] != -1:
                answer = str(self.answers[idx])
            correctAnswer = eval(question)
            report.append((question, answer, str(correctAnswer)))
        return report

