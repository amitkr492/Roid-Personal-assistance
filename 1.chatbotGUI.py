# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatbotGui.ui'
#
# Created: Sat Apr 23 10:41:24 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
from chatbot import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 304)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.askBtn = QtGui.QPushButton(Form)
        self.askBtn.setObjectName(_fromUtf8("askBtn"))
        self.horizontalLayout_3.addWidget(self.askBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Roid - Your Assistant", None))
        self.askBtn.setText(_translate("Form", "Put On!", None))
        self.askBtn.clicked.connect(self.getSolution)        #Here when click the button then calling getsolution of this file
        self.lineEdit.returnPressed.connect(self.getSolution)

    def getSolution(self):
        ques = self.lineEdit.text()      #fetching the question from the textbox
        self.lineEdit.setText("")

        #printing the question to dialogue box
        #print(ques)
        ans = chatBotResponse(str(ques))     #Here we are callig chatBotResponse for finding the answer.
        ques = "<div style='color:green;'><b>You: </b>"+str(ques)+"</div>"
        ques = ques.encode('utf-8')
        self.textBrowser.append(ques)

        
        ans = ans.encode('utf-8')
        ans = "<div style='color:blue;'><b>Roid: </b>"+str(ans)+"</div><br>"
        
        self.textBrowser.append(ans)
        scrollBar = self.textBrowser.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())