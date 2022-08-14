from PyQt5 import QtCore, QtGui, QtWidgets
import resources
import sys
import sqlite3
from menu import Ui_Menu
from notification import Ui_Dialog





class Ui_MainWindow(object):
    def popup_error(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi_notification(Dialog)
        Dialog.show()
    def popup_signup(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi_notification(Dialog)
        ui.change_index()
        Dialog.show()

    def set_name_n_surname(self,current_user):
        conn = sqlite3.connect('handler/users.db')
        cur = conn.cursor()
        result = []

        name = cur.execute("SELECT first_name FROM users WHERE username = ?",(current_user,)).fetchone()[0]
        surname = cur.execute("SELECT last_name FROM users WHERE username = ?", (current_user,)).fetchone()[0]

        result.append(name)
        result.append(surname)
        return result


    def open_menu(self,current_user):
        MainWindow.close()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Menu()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.label_21.setText(current_user[0])
        self.ui.label_20.setText(current_user[1])



    def signin_function(self):
        user = self.signin_username_line.text()
        password = self.signin_password_line.text()
        if not user or not password:
            self.popup_error()
        else:
            try:
                conn = sqlite3.connect('handler/users.db')
                cur = conn.cursor()
                cur.execute("SELECT password FROM users WHERE username=?;", (user,))
                result_pass = cur.fetchone()[0]
                if result_pass == password:
                    conn.commit()
                    conn.close()
                    args = self.set_name_n_surname(user)
                    self.open_menu(args)
                else:
                    self.popup_error()
            except:
                self.popup_error()

    def signup_function(self):
        user = str(self.signup_username_line.text())
        passw = str(self.signup_password_line.text())
        first_name = str(self.signup_firstname_line.text())
        last_name = str(self.signup_lastname_line.text())
        if not user or not passw:
            self.popup_error()
        else:
            conn = sqlite3.connect('handler/users.db')
            cur = conn.cursor()
            cur.execute(f"INSERT INTO users (username, password,first_name, last_name) VALUES (?,?,?,?)", (user,passw,first_name,last_name))
            conn.commit()
            conn.close()
            self.popup_signup()
            self.stackedWidget.setCurrentIndex(0)




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setFixedSize(800, 600)
        MainWindow.setStyleSheet("border-image: url(:/resourses/images/background.png);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(230, 180, 361, 351))
        self.stackedWidget.setStyleSheet("border-image:none;\n"
                                         "background-color:transparent")
        self.stackedWidget.setObjectName("stackedWidget")
        self.signin_page = QtWidgets.QWidget()
        self.signin_page.setStyleSheet("border-image:none;\n"
                                       "")
        self.signin_page.setObjectName("signin_page")
        self.signin_frame = QtWidgets.QFrame(self.signin_page)
        self.signin_frame.setGeometry(QtCore.QRect(0, 0, 351, 321))
        self.signin_frame.setStyleSheet("border-image: url(:/resourses/images/SignInStatic.png);\n"
                                        "background-color:transparent")
        self.signin_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signin_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signin_frame.setObjectName("signin_frame")
        self.signin_button = QtWidgets.QPushButton(self.signin_frame)
        self.signin_button.setGeometry(QtCore.QRect(50, 255, 251, 31))
        self.signin_button.setStyleSheet("QPushButton{\n"
                                         "border-image: url(:/resourses/images/sign_in_button.png);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "    border-image: url(:/resourses/images/sign_in_button_hovered.png);\n"
                                         "}\n"
                                         "QPushButton:pressed{\n"
                                         "\n"
                                         "    border-image: url(:/resourses/images/sign_in_button_pushed.png);\n"
                                         "}")
        self.signin_button.setText("")
        self.signin_button.setObjectName("signin_button")
        self.signin_password_line = QtWidgets.QLineEdit(self.signin_frame)
        self.signin_password_line.setGeometry(QtCore.QRect(80, 170, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        self.signin_password_line.setFont(font)
        self.signin_password_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                "color: rgb(116, 116, 116);\n"
                                                "padding-left:  10px\n"
                                                "")
        self.signin_password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signin_password_line.setObjectName("signin_password_line")
        self.signin_username_line = QtWidgets.QLineEdit(self.signin_frame)
        self.signin_username_line.setGeometry(QtCore.QRect(80, 120, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        self.signin_username_line.setFont(font)
        self.signin_username_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                "color: rgb(116, 116, 116);\n"
                                                "padding-left:  10px\n"
                                                "")
        self.signin_username_line.setCursorPosition(0)
        self.signin_username_line.setObjectName("signin_username_line")
        self.signup_page_button = QtWidgets.QPushButton(self.signin_frame)
        self.signup_page_button.setGeometry(QtCore.QRect(174, 20, 161, 51))
        self.signup_page_button.setStyleSheet("border:none;"
                                              "border-image:none;")
        self.signup_page_button.setText("")
        self.signup_page_button.setObjectName("signup_page_button")
        self.stackedWidget.addWidget(self.signin_page)
        self.signup_page = QtWidgets.QWidget()
        self.signup_page.setStyleSheet("border-image:none;\n"
                                       "background-color:transparent;")
        self.signup_page.setObjectName("signup_page")
        self.signup_frame = QtWidgets.QFrame(self.signup_page)
        self.signup_frame.setGeometry(QtCore.QRect(0, 0, 351, 351))
        self.signup_frame.setStyleSheet("border-image: url(:/resourses/images/SignUpStatic.png);\n"
                                        "background-color:transparent")
        self.signup_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.signup_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.signup_frame.setObjectName("signup_frame")
        self.signup_firstname_line = QtWidgets.QLineEdit(self.signup_frame)
        self.signup_firstname_line.setGeometry(QtCore.QRect(48, 90, 113, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        font.setBold(True)
        self.signup_firstname_line.setFont(font)
        self.signup_firstname_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                 "padding-left:10px;\n"
                                                 "color: rgb(116, 116, 116);")
        self.signup_firstname_line.setObjectName("signup_firstname_line")
        self.signup_lastname_line = QtWidgets.QLineEdit(self.signup_frame)
        self.signup_lastname_line.setGeometry(QtCore.QRect(185, 90, 113, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        font.setBold(True)
        self.signup_lastname_line.setFont(font)
        self.signup_lastname_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                "padding-left:10px;\n"
                                                "color: rgb(116, 116, 116);")
        self.signup_lastname_line.setObjectName("signup_lastname_line")
        self.signup_username_line = QtWidgets.QLineEdit(self.signup_frame)
        self.signup_username_line.setGeometry(QtCore.QRect(48, 130, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        font.setBold(True)
        self.signup_username_line.setFont(font)
        self.signup_username_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                "padding-left:10px;\n"
                                                "color: rgb(116, 116, 116);")
        self.signup_username_line.setObjectName("signup_username_line")
        self.signup_password_line = QtWidgets.QLineEdit(self.signup_frame)
        self.signup_password_line.setGeometry(QtCore.QRect(48, 170, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        font.setBold(True)
        self.signup_password_line.setFont(font)
        self.signup_password_line.setStyleSheet("border-image: url(:/resourses/images/qline.png);\n"
                                                "padding-left:10px;\n"
                                                "color: rgb(116, 116, 116);")
        self.signup_password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_password_line.setObjectName("signup_password_line")
        self.switch_frame = QtWidgets.QFrame(self.signup_frame)
        self.switch_frame.setGeometry(QtCore.QRect(48, 210, 251, 25))
        self.switch_frame.setStyleSheet("border-image: url(:/resourses/images/DoctorPatientSwitchP.png);")
        self.switch_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.switch_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.switch_frame.setObjectName("switch_frame")
        self.patient_button = QtWidgets.QRadioButton(self.switch_frame)
        self.patient_button.setGeometry(QtCore.QRect(4, 0, 121, 24))
        self.patient_button.setStyleSheet("QRadioButton{\n"
                                          "border-image:none}\n"
                                          "QRadioButton::indicator {\n"
                                          "width: 0px;\n"
                                          " height: 0px;\n"
                                          "}")
        self.patient_button.setText("")
        self.patient_button.setObjectName("patient_button")
        self.doctor_button = QtWidgets.QRadioButton(self.switch_frame)
        self.doctor_button.setGeometry(QtCore.QRect(124, 0, 131, 24))
        self.doctor_button.setStyleSheet("QRadioButton{\n"
                                         "border-image:none}\n"
                                         "QRadioButton::indicator {\n"
                                         "width: 0px;\n"
                                         " height: 0px;\n"
                                         "}")
        self.doctor_button.setText("")
        self.doctor_button.setObjectName("doctor_button")
        self.male_button = QtWidgets.QRadioButton(self.signup_frame)
        self.male_button.setGeometry(QtCore.QRect(55, 253, 20, 20))
        self.male_button.setStyleSheet("QRadioButton {\n"
                                       "    border-image: url(:/resourses/images/checkbox.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator {\n"
                                       "    width: 20px;\n"
                                       "    height: 20px;\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:unchecked {\n"
                                       "    \n"
                                       "    \n"
                                       "    border-image: url(:/resourses/images/checkbox.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:unchecked:hover {\n"
                                       "    border-image: url(:/resourses/images/checkbox_hover.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:unchecked:pressed {\n"
                                       "    \n"
                                       "    border-image: url(:/resourses/images/checkbox_checked.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:checked {\n"
                                       "    \n"
                                       "    border-image: url(:/resourses/images/checkbox_checked.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:checked:hover {\n"
                                       "    \n"
                                       "    border-image: url(:/resourses/images/checkbox_hover.png);\n"
                                       "}\n"
                                       "\n"
                                       "QRadioButton::indicator:checked:pressed {\n"
                                       "    border-image: url(:/resourses/images/checkbox.png);\n"
                                       "}")
        self.male_button.setText("")
        self.male_button.setObjectName("radioButton")
        self.female_button = QtWidgets.QRadioButton(self.signup_frame)
        self.female_button.setGeometry(QtCore.QRect(145, 253, 20, 20))
        self.female_button.setStyleSheet("QRadioButton {\n"
                                         "    border-image: url(:/resourses/images/checkbox.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator {\n"
                                         "    width: 20px;\n"
                                         "    height: 20px;\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:unchecked {\n"
                                         "    \n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/checkbox.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:unchecked:hover {\n"
                                         "    border-image: url(:/resourses/images/checkbox_hover.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:unchecked:pressed {\n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/checkbox_checked.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:checked {\n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/checkbox_checked.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:checked:hover {\n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/checkbox_hover.png);\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator:checked:pressed {\n"
                                         "    border-image: url(:/resourses/images/checkbox.png);\n"
                                         "}")
        self.female_button.setText("")
        self.female_button.setObjectName("radioButton_2")
        self.signup_button = QtWidgets.QPushButton(self.signup_frame)
        self.signup_button.setGeometry(QtCore.QRect(48, 290, 251, 33))
        self.signup_button.setStyleSheet("QPushButton{\n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/signup_button.png);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "    \n"
                                         "    border-image: url(:/resourses/images/sign_up_hover.png);\n"
                                         "}\n"
                                         "QPushButton:pressed{\n"
                                         "    border-image: url(:/resourses/images/sign_up_pushed.png);\n"
                                         "}")
        self.signup_button.setText("")
        self.signup_button.setObjectName("signup_button")
        self.signin_page_button = QtWidgets.QPushButton(self.signup_frame)
        self.signin_page_button.setGeometry(QtCore.QRect(20, 20, 151, 51))
        self.signin_page_button.setStyleSheet("border:none;"
                                              "border-image:none;")
        self.signin_page_button.setText("")
        self.signin_page_button.setObjectName("signin_page_button")
        self.stackedWidget.addWidget(self.signup_page)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ##CODE
        self.signup_page_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.signin_page_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.doctor_button.clicked.connect(
            lambda: self.switch_frame.setStyleSheet("border-image: url(:/resourses/images/DoctorPatientSwitchD.png);"))
        self.patient_button.clicked.connect(
            lambda: self.switch_frame.setStyleSheet("border-image: url(:/resourses/images/DoctorPatientSwitchP.png);"))
        self.doctor_patient_group = QtWidgets.QButtonGroup(MainWindow)
        self.doctor_patient_group.setObjectName("doctor_patient_group")
        self.doctor_patient_group.addButton(self.patient_button)
        self.doctor_patient_group.addButton(self.doctor_button)
        self.male_female_group = QtWidgets.QButtonGroup(MainWindow)
        self.male_female_group.setObjectName("male_female_group")
        self.male_female_group.addButton(self.male_button)
        self.male_female_group.addButton(self.female_button)
        self.signin_button.clicked.connect(self.signin_function)
        self.signup_button.clicked.connect(self.signup_function)







        ## CODE

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signin_password_line.setPlaceholderText(_translate("MainWindow", "Пароль"))
        self.signin_username_line.setPlaceholderText(_translate("MainWindow", "Ім'я користувача"))
        self.signup_firstname_line.setPlaceholderText(_translate("MainWindow", "Ім'я"))
        self.signup_lastname_line.setPlaceholderText(_translate("MainWindow", "Прізвище"))
        self.signup_username_line.setPlaceholderText(_translate("MainWindow", "Ім'я користувача"))
        self.signup_password_line.setPlaceholderText(_translate("MainWindow", "Пароль"))





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
