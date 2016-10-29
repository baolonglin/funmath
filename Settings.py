from PyQt5.QtCore import QSettings


class Settings:

    def __init__(self):
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

    def getMaxNum(self):
        return self.settings.value('max', 100, type=int)

    def setMaxNum(self, v):
        self.settings.setValue('max', v)

    def getMinNum(self):
        return self.settings.value('min', 0, type=int)

    def setMinNum(self, v):
        self.settings.setValue('min', v)

    def isPlusEnable(self):
        return self.settings.value('op_plus', True, type=bool)

    def setPlusEnable(self, v):
        self.settings.setValue('op_plus', v)

    def isMinusEnable(self):
        return self.settings.value('op_minus', True, type=bool)

    def setMinusEnable(self, v):
        self.settings.setValue('op_minus', v)

    def isMultiEnable(self):
        return self.settings.value('op_multi', False, type=bool)

    def setMultiEnable(self, v):
        self.settings.setValue('op_multi', v)

    def isDivideEnable(self):
        return self.settings.value('op_div', False, type=bool)

    def setDivideEnable(self, v):
        self.settings.setValue('op_div', v)

    def getQuestionNum(self):
        return self.settings.value('question_number', 15, type=int)

    def setQuestionNum(self, v):
        self.settings.setValue('question_number', v)

    def getOperatorNum(self):
        return self.settings.value('op_number', 1, type=int)

    def setOperatorNum(self, v):
        self.settings.setValue('op_number', v)
