from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):


    def setupUi_notification(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(306, 225)
        Dialog.setFixedSize(306, 225)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.stackedNotifications = QtWidgets.QStackedWidget(Dialog)
        self.stackedNotifications.setGeometry(QtCore.QRect(0, 0, 306, 225))
        self.stackedNotifications.setStyleSheet("background-color:white")
        self.stackedNotifications.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(10, 30, 101, 191))
        self.label.setStyleSheet("border-image: url(:/resourses/images/doctor.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(130, 50, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet('color:black')
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setGeometry(QtCore.QRect(130, 180, 131, 24))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{border-radius:7px;\n"
"color:white;\n"
"background-color:rgb(0,98,185)\n}"
"QPushButton:hover{"
                                      "background-color:rgb(30,130,185)}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: Dialog.close())
        self.stackedNotifications.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setGeometry(QtCore.QRect(8, 30, 91, 191))
        self.label_3.setStyleSheet("border-image: url(:/resourses/images/doctor2.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setGeometry(QtCore.QRect(110, 40, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet('color:black')
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 180, 131, 24))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{border-radius:7px;\n"
        
"color:white;\n"
"background-color:rgb(87,194,162)}\n"
"\n"
"QPushButton:hover{"
                                        "background-color:rgb(105,194,172)"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: Dialog.close())
        self.stackedNotifications.addWidget(self.page_2)

        self.retranslateUi(Dialog)
        self.stackedNotifications.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def change_index(self):
        self.stackedNotifications.setCurrentIndex(1)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Щось пішло не так..."))
        self.pushButton.setText(_translate("Dialog", "Гаразд"))
        self.label_4.setText(_translate("Dialog", "Реєстрація успішна!"))
        self.pushButton_2.setText(_translate("Dialog", "Гаразд"))
        Dialog.setWindowIcon(QtGui.QIcon('warning.png'))





class in_development_window(Ui_Dialog):

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "В розробці..."))
        self.pushButton.setText(_translate("Dialog", "Гаразд"))
        self.label_4.setText(_translate("Dialog", "Реєстрація успішна!"))
        self.pushButton_2.setText(_translate("Dialog", "Гаразд"))
        Dialog.setWindowIcon(QtGui.QIcon('in_Dev.png'))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi_notification(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
