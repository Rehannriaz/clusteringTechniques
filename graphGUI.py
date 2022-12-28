from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter
import CS221_SemesterProject as TM
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


class Ui_Form(object):

    def setupUi(self, Form):
        self.COUNTER = 0
        self.Threshold1 = 0
        Form.setObjectName("Graphing_Window")
        Form.resize(929, 787)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 70, 640, 480))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.NextButton = QtWidgets.QPushButton(Form)
        self.NextButton.setGeometry(QtCore.QRect(620, 640, 161, 51))
        self.NextButton.setObjectName("NextButton")
        self.PrevPicure = QtWidgets.QPushButton(Form)
        self.PrevPicure.setGeometry(QtCore.QRect(130, 640, 161, 51))
        self.PrevPicure.setObjectName("PrevPicure")
        self.loadTask3 = QtWidgets.QPushButton(Form)
        self.loadTask3.setGeometry(QtCore.QRect(370, 640, 161, 51))
        self.loadTask3.setObjectName("loadTask3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(360, 711, 171, 31))
        self.TresholdLabel = QtWidgets.QLabel(Form)
        self.TresholdLabel.setGeometry(QtCore.QRect(220, 710, 131, 31))
        self.TresholdLabel.setObjectName("TresholdLabel: ")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaxLength(5)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.EnterButton = QtWidgets.QPushButton(Form)
        self.EnterButton.setGeometry(QtCore.QRect(540, 710, 101, 31))
        self.EnterButton.clicked.connect(self.show_line)
        self.EnterButton.setObjectName("EnterButton")

        self.PrevPicure.clicked.connect(
            self.displayPrevPicture)
        self.NextButton.clicked.connect(
            self.displayNextPicture)
        self.loadTask3.clicked.connect(self.RUN_task3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_line(self):
            self.Threshold1=TM.getThreshold(self.lineEdit.text())
    def RUN_task3(self):
        TM.Task3(TM.permuteMatrix(TM.fileReader()),self.Threshold1)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.loadTask3.setText(_translate("Form", "RUN TASK 3"))
        self.NextButton.setText(_translate("Form", "NextPicture"))
        self.PrevPicure.setText(_translate("Form", "PrevPicture"))
        self.EnterButton.setText(_translate("Form", "Enter"))

    def displayNextPicture(self):
        fileName = "Graphpng\graph"+str(self.COUNTER)+".png"
        self.COUNTER += 1
        img = cv.imread(fileName)
        if (img is None):
            print("Error, File does not exist")
            self.label.setText("Error, File does not exist")
            return
        # plt.imshow(img)
        # plt.show()
        self.label.setGeometry(QtCore.QRect(130, 70, 640, 480))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(fileName))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

    def displayPrevPicture(self):
        self.COUNTER -= 1
        fileName = "Graphpng\graph"+str(self.COUNTER)+".png"
        img = cv.imread(fileName)
        if (img is None):
            print("Error, File does not exist")
            self.label.setText("Error, File does not exist")
            return
        # plt.imshow(img)
        # plt.show()
        self.label.setGeometry(QtCore.QRect(130, 70, 640, 480))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(fileName))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
