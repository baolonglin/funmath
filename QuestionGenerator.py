
from enum import Enum
import random

class Operator(Enum):
    plus = 1
    minus = 2
    multiply = 3
    divide = 4

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
        if self.settings.isPlusEnable():
            self.supportedOp.append(Operator.multiply)
        if self.settings.isDivideEnable():
            self.supportedOp.append(Operator.divide)

    def getRandNum(self):
        return random.randint(self.settings.getMinNum(),
                              self.settings.getMaxNum())
    def getRandOp(self):
        return self.supportedOp[
            random.randint(0, len(self.supportedOp) - 1)]

    def initQuestion(self):
        for q_idx in range(self.settings.getQuestionNum()):
            question = []
            for i_idx in range(self.settings.getOperatorNum()):
                question.append(self.getRandNum())
                question.append(self.getRandOp())
            question.append(self.getRandNum())
            self.generatedQuestions.append(question)
            self.answers.append(-1)

    def curr(self):
        return self.generatedQuestions[self.current_question_idx], self.answers[self.current_question_idx]

    def updateCurrentQuestionAnswer(self, answer):
        if self.current_question_idx < len(self.generatedQuestions):
            self.answers[self.current_question_idx] = answer

    def previous(self, answer):
        self.updateCurrentQuestionAnswer(answer)
        self.current_question_idx -= 1
        if self.current_question_idx > 0:
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
