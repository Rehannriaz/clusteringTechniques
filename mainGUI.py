

from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter
import CS221_SemesterProject as TM
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from graphGUI import Ui_Form


class Ui_MainWindow(object):
         
    def setupUi(self, MainWindow):
        
        
        MainWindow.setObjectName("Main")
        MainWindow.resize(855, 649)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.printOutput = QtWidgets.QPushButton(self.centralwidget)
        self.printOutput.setGeometry(QtCore.QRect(230, 10, 151, 41))
        self.printOutput.setObjectName("printOutput")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.printOutput_color = QtWidgets.QPushButton(self.centralwidget)
        self.printOutput_color.setGeometry(QtCore.QRect(230, 60, 151, 41))
        self.printOutput_color.setObjectName("printOutput_color")
        self.TASK1Button = QtWidgets.QPushButton(self.centralwidget)
        self.TASK1Button.setGeometry(QtCore.QRect(40, 10, 161, 91))
        self.TASK1Button.setObjectName("TASK1Button")
        self.TASK1Button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.TASK1Button_2.setGeometry(QtCore.QRect(40, 150, 161, 91))
        self.TASK1Button_2.setObjectName("TASK1Button_2")
        self.TASK1Button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.TASK1Button_3.setGeometry(QtCore.QRect(40, 290, 161, 91))
        self.TASK1Button_3.setObjectName("TASK1Button_3")
        self.TASK1Button.clicked.connect(self.Task1_ButtonClicked)
        self.TASK1Button_2.clicked.connect(self.Task2_ButtonClicked)
        self.TASK1Button_3.clicked.connect(self.Task3_ButtonClicked)
        self.printOutput.clicked.connect(self.displayDiscreteButton)
        self.printOutput_color.clicked.connect(self.displayColoredButton)
    

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionInsert_File = QtWidgets.QAction(MainWindow)
        self.actionInsert_File.setObjectName("actionInsert_File")
        self.menuFile.addAction(self.actionInsert_File)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TASK1Button.setText(_translate("MainWindow", "RUN TASK 1"))
        self.TASK1Button_2.setText(_translate("MainWindow", "RUN TASK 2"))
        self.TASK1Button_3.setText(_translate("MainWindow", "RUN TASK 3"))
        self.printOutput_color.setText(_translate(
            "MainWindow", "Print GreenColorCoded"))
        self.printOutput.setText(_translate("MainWindow", "PrintOutput"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionInsert_File.setText(_translate("MainWindow", "Insert Data"))


    def Task1_ButtonClicked(self):
        TM.Task1(TM.fileReader())

    def Task2_ButtonClicked(self):
        TM.Task2(TM.fileReader())

    def Task3_ButtonClicked(self):
        self.window=QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()
        
        
        

    def displayColoredButton(self):
        fileName = "GreenColorCoded1.png"
        img = cv.imread(fileName)
        if img is None:
            self.label.setText("Error, File does not exist")
            print("file does not exist")
            return
        plt.imshow(img)
        plt.show()
        self.label.setGeometry(QtCore.QRect(380, 30, 421, 371))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(fileName))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")


    def displayDiscreteButton(self):
        fileName = "discretizedMatrix.png"
        img = cv.imread(fileName)
        if (img is None):
            print("Error, File does not exist")
            self.label.setText("Error, File does not exist")
            return    
        plt.imshow(img)
        plt.show()
        self.label.setGeometry(QtCore.QRect(380, 30, 421, 371))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(fileName))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
     
 





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
