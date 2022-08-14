import cmath

from PyQt5 import QtCore, QtGui, QtWidgets
from db_func import *
from back import *
from notification import Ui_Dialog, in_development_window
import sqlite3
import webbrowser



class CompleterDelegate( QtWidgets.QStyledItemDelegate ):
    def initStyleOption(self, option, index):
        super( CompleterDelegate, self ).initStyleOption( option, index )
        # option.font.setFamily('Montserrat')
        # option.palette.setBrush(QtGui.QPalette.Text, QtGui.QColor(112,112,112))
        option.font.setBold( True )
        option.displayAlignment = QtCore.Qt.AlignCenter


class Ui_Menu(object):
    def doctor_recommendation(self):
        print('1')
        self.Doctor_1_Categories = [self.Doctor_1_Category_1.text(), self.Doctor_1_Category_2.text(), self.Doctor_1_Category_3.text()]
        self.Doctor_2_Categories = [self.Doctor_2_Category_1.text(), self.Doctor_2_Category_2.text(), self.Doctor_2_Category_3.text()]
        print('2')
        print(self.type1)
        print(self.Doctor_1_Categories)
        print(self.Doctor_2_Categories)
        if self.type1 in self.Doctor_1_Categories:
            print('hello')
            self.recommended_doctor_image.setStyleSheet("border-image: url(:/resource/images/doctor_example.png);")
            self.recommended_name.setText(self.Name_1.text())
            self.recommended_experience.setText(self.Doctor_1_Experience.text())
            self.recommended_label.setText('Рекомендований лікар:')
        elif self.type1 in self.Doctor_2_Categories:
            print(self.Doctor_2_Name.text(), self.Doctor_2_Experience.text())
            self.recommended_doctor_image.setStyleSheet('border-image: url(:/resource/images/doctor_example_2.jpg);')
            self.recommended_name.setText(self.Doctor_2_Name.text())
            self.recommended_experience.setText(self.Doctor_2_Experience.text())
            self.recommended_label.setText('Рекомендований лікар:')
        else:
            self.recommended_doctor_image.setStyleSheet('border-image:none;')
            self.recommended_name.setText('')
            self.recommended_experience.setText('')
            self.recommended_label.setText('На жаль, нам не вдалось знайти лікаря для вас :(')





    def unavailable(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi_notification(Dialog)
        Dialog.show()


    def in_development(self):
        Dialog = QtWidgets.QDialog()
        ui = in_development_window()
        ui.setupUi_notification(Dialog)
        Dialog.show()

    def move_to_house(self):
        self.frame.setStyleSheet("border-image: url(:/resource/images/bar_house.png);")
        self.stackedWidget.setCurrentIndex(3)

    def move_to_diagnostics(self):
        self.frame.setStyleSheet("border-image: url(:/resource/images/bar_diagnostics.png);")
        self.stackedWidget.setCurrentIndex(0)

    def move_to_doctors(self):
        self.frame.setStyleSheet("border-image: url(:/resource/images/bar_doctors.png);")
        self.stackedWidget.setCurrentIndex(5)

    def move_to_doctors_from_diagnostics(self):
        self.frame.setStyleSheet("border-image: url(:/resource/images/bar_doctors.png);")
        self.extra_symptoms_list.clear()
        self.selected_symptoms_list_postdiagnostic.clear()
        self.stackedWidget.setCurrentIndex(5)

    def show_info(self, info, type = 'Фіг його знає'):
        self.stackedWidget.setCurrentIndex(2)
    def update_symptoms(self):
        self.selected_symptoms = [self.selected_symptoms_list.item(i).text() for i in
                                  range(self.selected_symptoms_list.count())]
        if self.extra_symptoms_list.selectedItems():
            self.extra_symptoms_selected = [item.text() for item in self.extra_symptoms_list.selectedItems()]
            self.updated_symptoms_lst = list(self.selected_symptoms + self.extra_symptoms_selected)
        else:
            self.updated_symptoms_lst = list(self.selected_symptoms)
        print(self.updated_symptoms_lst)
        self.selected_symptoms_list_postdiagnostic.clear()
        for i in range(len(self.updated_symptoms_lst)):
            item = QtWidgets.QListWidgetItem()
            self.selected_symptoms_list_postdiagnostic.addItem(item)
        for i in range(len(self.updated_symptoms_lst)):
            item = self.selected_symptoms_list_postdiagnostic.item(i)
            item.setText(self.updated_symptoms_lst[i])
    def fill_extra_symptoms(self, selected_sympt, diseases):
        self.extrasymp_lst = list(get_filtered_symps(selected_sympt, diseases))
        for i in range(len(self.extrasymp_lst)):
            item = QtWidgets.QListWidgetItem()
            self.extra_symptoms_list.addItem(item)
        for i in range(len(self.extrasymp_lst)):
            item = self.extra_symptoms_list.item(i)
            item.setText(self.extrasymp_lst[i])

    def func(self, diseases, selected2_symptoms):
        self.info_dict = set_precents(diseases)
        sorted_dict = {}
        sorted_keys = sorted( self.info_dict, key=self.info_dict.get)  # [1, 3, 2]
        sorted_keys = reversed( sorted_keys )

        for w in sorted_keys:
            sorted_dict[w] = self.info_dict[w]

        if len(diseases) >= 3:
            self.first_disease_name.setText(list(sorted_dict.keys())[0])
            dis_1 = self.first_disease_name.text()
            self.label_25.setText(dis_1)
            self.first_disease_pbar.setValue(sorted_dict[list(sorted_dict.keys())[0]][0])
            self.first_disease_button.clicked.connect(lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[0]][1]))
            self.first_disease_button.clicked.connect(self.show_info)

            self.second_disease_name.setText( list( sorted_dict.keys() )[1] )
            dis_2 = self.second_disease_name.text()
            self.label_26.setText(dis_2)
            self.second_disease_pbar.setValue( sorted_dict[list( sorted_dict.keys() )[1]][0] )
            self.second_disease_button.clicked.connect(
                lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[1]][1]))
            self.second_disease_button.clicked.connect(self.show_info)
            self.third_disease_name.setText( list( sorted_dict.keys() )[2] )
            self.third_disease_pbar.setValue( sorted_dict[list( sorted_dict.keys() )[2]][0] )
            self.third_disease_button.clicked.connect(
                lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[2]][1]))
            self.third_disease_button.clicked.connect(self.show_info)
            for obj in gc.get_objects():
                if isinstance(obj, Disease):
                   if obj.name == list(sorted_dict.keys())[0]:
                        self.type1 = obj.type
                   elif obj.name == list(sorted_dict.keys())[1]:
                        self.type2 = obj.type
                   elif obj.name == list(sorted_dict.keys())[2]:
                        self.type3 = obj.type
            self.first_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type1))
            self.second_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type2))
            self.third_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type3))
        elif len(diseases) == 2:
            self.first_disease_name.setText(list(sorted_dict.keys())[0])
            self.first_disease_pbar.setValue(sorted_dict[list(sorted_dict.keys())[0]][0])
            self.first_disease_button.clicked.connect(
                lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[0]][1]))
            self.first_disease_button.clicked.connect(self.show_info)

            self.second_disease_name.setText(list(sorted_dict.keys())[1])
            self.second_disease_pbar.setValue(sorted_dict[list(sorted_dict.keys())[1]][0])
            self.second_disease_button.clicked.connect(
                lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[1]][1]))
            self.second_disease_button.clicked.connect(self.show_info)
            for obj in gc.get_objects():
                if isinstance(obj, Disease):
                    if obj.name == list(sorted_dict.keys())[0]:
                        self.type1 = obj.type
                    elif obj.name == list(sorted_dict.keys())[1]:
                        self.type2 = obj.type
            self.first_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type1))
            self.second_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type2))
            self.third_disease_pbar.hide()
            self.third_disease_name.hide()
            self.third_disease_button.hide()
            self.third_disease_icon_frame.hide()
        elif len(diseases) == 1:
            self.first_disease_name.setText(list(sorted_dict.keys())[0])
            self.first_disease_pbar.setValue(sorted_dict[list(sorted_dict.keys())[0]][0])
            self.first_disease_button.clicked.connect(
                lambda: self.disease_info_text_browser.setText(sorted_dict[list(sorted_dict.keys())[0]][1]))
            self.first_disease_button.clicked.connect(self.show_info)
            for obj in gc.get_objects():
                if isinstance(obj, Disease):
                   if obj.name == list(sorted_dict.keys())[0]:
                        self.type1 = obj.type

            self.first_disease_button.clicked.connect(lambda: self.disease_type_label.setText(self.type1))
            self.third_disease_pbar.hide()
            self.third_disease_name.hide()
            self.third_disease_button.hide()
            self.third_disease_icon_frame.hide()
            self.second_disease_pbar.hide()
            self.second_disease_name.hide()
            self.second_disease_button.hide()
            self.second_disease_icon_frame.hide()
            print('hello')
        self.doctor_recommendation()
    def recalculation(self):
        self.selected_symptoms = [self.selected_symptoms_list_postdiagnostic.item( i ).text() for i in
                                  range( self.selected_symptoms_list_postdiagnostic.count())]
        print(self.selected_symptoms)
        self.potential_diseases = diagnose_suggestions(self.selected_symptoms)
        self.func(self.potential_diseases, self.selected_symptoms)
        conn = sqlite3.connect( 'diseases.db' )
        c = conn.cursor()
        c.execute( 'UPDATE symptoms SET points = 0' )
        c.execute( 'UPDATE Diseases SET points = 0' )
        conn.commit()
        conn.close()



    def search_symptom(self):
        try:
            text = self.search_line.text()
            ind = [self.symptoms_list.item( i ).text() for i in range( self.symptoms_list.count() )].index( text )
            self.symptoms_list.setCurrentRow(ind)
        except:
            print('Empty line')

    def diagnosis_run(self):
        self.selected_symptoms = [self.selected_symptoms_list.item( i ).text() for i in
                                  range( self.selected_symptoms_list.count() )]
        if self.selected_symptoms:
            self.potential_diseases = diagnose_suggestions(self.selected_symptoms)
            self.stackedWidget.setCurrentIndex(1)
            for i in range(len(self.selected_symptoms)):
                    item = QtWidgets.QListWidgetItem()
                    self.selected_symptoms_list_postdiagnostic.addItem(item)
            for i in range(len(self.selected_symptoms)):
                    item = self.selected_symptoms_list_postdiagnostic.item(i)
                    item.setText(self.selected_symptoms[i])
            self.func(self.potential_diseases, self.selected_symptoms)
            self.fill_extra_symptoms(self.selected_symptoms, self.potential_diseases)
            conn = sqlite3.connect( 'diseases.db' )
            c = conn.cursor()
            c.execute( 'UPDATE symptoms SET points = 0' )
            c.execute( 'UPDATE Diseases SET points = 0' )
            conn.commit()
            conn.close()
            # self.create_report(self.potential_diseases)
        else:
            Dialog = QtWidgets.QDialog()
            ui = Ui_Dialog()
            ui.setupUi_notification( Dialog )
            Dialog.show()

    def get_data(self, model):
        model.setStringList( all_symptoms )

    def move_symptom(self):
        selected = self.symptoms_list.currentItem().text()
        item = QtWidgets.QListWidgetItem()
        self.symptoms_list.takeItem( self.symptoms_list.currentRow() )
        self.selected_symptoms_list.addItem( item )
        item.setText( selected )
        self.symptoms_list.clearSelection()

    def delete_symptom(self):
        selected = self.selected_symptoms_list.currentItem().text()
        item = QtWidgets.QListWidgetItem()
        self.selected_symptoms_list.takeItem( self.selected_symptoms_list.currentRow() )
        self.symptoms_list.addItem( item )
        item.setText( selected )
        self.symptoms_list.clearSelection()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1600, 900))
        MainWindow.setStyleSheet("QScrollBar:vertical {\n"
"                                 boder:none;\n"
"                                 border-image: url(:/resource/images/scroll_bg.png);\n"
"                                 margin: 20px 0 20px 0;\n"
"                                 boder-radius:0px;\n"
"                                 }\n"
"                                 QScrollBar::handle:vertical {\n"
"                                 background-color: rgb(0, 170, 127);\n"
"                                 border-radius: 8px;\n"
"                                 }\n"
"                                  QScrollBar::add-line:vertical {\n"
"                                      border: none;\n"
"                                      \n"
"                                     \n"
"                                  }\n"
"                                 QScrollBar::sub-line:vertical {\n"
"                                      border: none;\n"
"                                     \n"
"                                  }\n"
"                                 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"                                      background: none;\n"
"                                    \n"
"                                 }\n"
"                                  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"                                      background: none;\n"
"                                  }\n"
"\n"
"QScrollBar:horizontal {\n"
"                                 boder:none;\n"
"                                 border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"                                 margin: 20px 20px 20px 20px;\n"
"                                 boder-radius:0px;\n"
"                                 }\n"
"                                 QScrollBar::handle:horizontal {\n"
"                                 background-color: rgb(0, 170, 127);\n"
"                                 border-radius: 7px;\n"
"                                 }\n"
"                                  QScrollBar::add-line:horizontal {\n"
"                                      border: none;\n"
"                                  }\n"
"                                 QScrollBar::sub-line:horizontal {\n"
"                                      border: none;\n"
"                                     \n"
"                                  }\n"
"                                 QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
"                                      background: none;\n"
"                                    \n"
"                                 }\n"
"                                  QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"                                      background: none;\n"
"                                  }\n"
"")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("border-image: url(:/resource/images/Background.svg);")
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, -30, 241, 951))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(241, 0))
        self.frame.setStyleSheet("border-image: url(:/resource/images/bar_house.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.house_page_button = QtWidgets.QPushButton(self.frame)
        self.house_page_button.setGeometry(QtCore.QRect(20, 63, 201, 41))
        self.house_page_button.setStyleSheet("border-image:none;\n"
"border:none;    ")
        self.house_page_button.setText("")
        self.house_page_button.setObjectName("house_page_button")
        self.diagnostics_page_button = QtWidgets.QPushButton(self.frame)
        self.diagnostics_page_button.setGeometry(QtCore.QRect(20, 110, 201, 41))
        self.diagnostics_page_button.setStyleSheet("border-image:none;\n"
"border:none;    ")
        self.diagnostics_page_button.setText("")
        self.diagnostics_page_button.setObjectName("diagnostics_page_button")
        self.statictics_page_button = QtWidgets.QPushButton(self.frame)
        self.statictics_page_button.setGeometry(QtCore.QRect(20, 160, 201, 41))
        self.statictics_page_button.setStyleSheet("border-image:none;\n"
"border:none;    ")
        self.statictics_page_button.setText("")
        self.statictics_page_button.setObjectName("statictics_page_button")
        self.doctors_page_button = QtWidgets.QPushButton(self.frame)
        self.doctors_page_button.setGeometry(QtCore.QRect(20, 210, 201, 41))
        self.doctors_page_button.setStyleSheet("border-image:none;\n"
"border:none;    ")
        self.doctors_page_button.setText("")
        self.doctors_page_button.setObjectName("doctors_page_button")
        self.my_acc_button = QtWidgets.QPushButton(self.frame)
        self.my_acc_button.setGeometry(QtCore.QRect(30, 720, 181, 51))
        self.my_acc_button.setStyleSheet("border-image:none;\n"
"border:none;    ")
        self.my_acc_button.clicked.connect(self.move_to_house)
        self.my_acc_button.setText("")
        self.my_acc_button.setObjectName("my_acc_button")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(240, 0, 1661, 1080))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setToolTip("")
        self.stackedWidget.setToolTipDuration(-1)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.diagnostic_page = QtWidgets.QWidget()
        self.diagnostic_page.setObjectName("diagnostic_page")
        self.search_line = QtWidgets.QLineEdit(self.diagnostic_page)
        self.search_line.setGeometry(QtCore.QRect(50, 10, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        font.setWeight(75)
        self.search_line.setFont(font)
        self.search_line.setStyleSheet("border-image: url(:/resource/images/search_bg.svg);\n"
"color: rgb(97, 97, 97);\n"
"padding-left:15px")
        self.search_line.setObjectName("search_line")
        self.frame_2 = QtWidgets.QFrame(self.diagnostic_page)
        self.frame_2.setGeometry(QtCore.QRect(30, 150, 561, 751))
        self.frame_2.setStyleSheet("border-image: url(:/resource/images/list_bg.png);\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.symptoms_list = QtWidgets.QListWidget(self.frame_2)
        self.symptoms_list.setGeometry(QtCore.QRect(60, 60, 441, 631))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.symptoms_list.setFont(font)
        self.symptoms_list.setToolTipDuration(-1)
        self.symptoms_list.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.symptoms_list.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                         background-color:rgb(87,194,163);\n"
"                                                 color: rgb(112, 112, 112);\n"
"                                                 color: rgb(255, 255, 255);\n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                        color:rgb(87,194,163);}\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                        border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;    \n"
"                                        \n"
"                                        border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"\n"
"                                        margin: 2px 5px 0 0px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{    \n"
"                                        background-color: rgb(231, 231, 232);\n"
"                                        border-radius: 10px;\n"
"                                        color: rgb(112, 112, 112);\n"
"                                        margin:  5px 10px 0 0;\n"
"                                        padding:3px;\n"
"                                        }")
        self.symptoms_list.setDragEnabled(True)
        self.symptoms_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.symptoms_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.symptoms_list.setTextElideMode(QtCore.Qt.ElideNone)
        self.symptoms_list.setFlow(QtWidgets.QListView.TopToBottom)
        self.symptoms_list.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.symptoms_list.setUniformItemSizes(False)
        self.symptoms_list.setWordWrap(True)
        self.symptoms_list.setSelectionRectVisible(False)
        self.symptoms_list.setObjectName("symptoms_list")
        self.frame_17 = QtWidgets.QFrame(self.frame_2)
        self.frame_17.setGeometry(QtCore.QRect(460, 660, 101, 91))
        self.frame_17.setStyleSheet("border-image: url(:/resource/images/decor_3.svg);")
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.frame_3 = QtWidgets.QFrame(self.diagnostic_page)
        self.frame_3.setGeometry(QtCore.QRect(850, 70, 451, 381))
        self.frame_3.setStyleSheet("border-image: url(:/resource/images/smaller_list_bg.png);\n"
"")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.selected_symptoms_list = QtWidgets.QListWidget(self.frame_3)
        self.selected_symptoms_list.setGeometry(QtCore.QRect(50, 60, 361, 261))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.selected_symptoms_list.setFont(font)
        self.selected_symptoms_list.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                           \n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                             }\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                            border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;\n"
"                                            \n"
"                                            border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 2px 5px 0 5px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{\n"
"                                        background-color: rgb(87,194,163);\n"
"                                        border-radius: 10px;    \n"
"                                        padding:3px;\n"
"                                        color: rgb(255, 255, 255);\n"
"                                        margin:  5px 15px 0 0;\n"
"                                        }")
        self.selected_symptoms_list.setDragEnabled(True)
        self.selected_symptoms_list.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.selected_symptoms_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.selected_symptoms_list.setTextElideMode(QtCore.Qt.ElideNone)
        self.selected_symptoms_list.setWordWrap(True)
        self.selected_symptoms_list.setObjectName("selected_symptoms_list")
        self.label_2 = QtWidgets.QLabel(self.diagnostic_page)
        self.label_2.setGeometry(QtCore.QRect(870, 40, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.search_button = QtWidgets.QPushButton(self.diagnostic_page)
        self.search_button.setGeometry(QtCore.QRect(520, 15, 31, 31))
        self.search_button.setStyleSheet("QPushButton{\n"
"    border-image: url(:/resource/images/searchbutton.svg);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/resource/images/searchbutton_hover.svg);\n"
"}")
        self.search_button.setText("")
        self.search_button.setObjectName("search_button")
        self.label_3 = QtWidgets.QLabel(self.diagnostic_page)
        self.label_3.setGeometry(QtCore.QRect(60, 110, 501, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border-image: none;\n"
"border-radius: 25px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.diagnostic_page)
        self.label.setGeometry(QtCore.QRect(720, 470, 631, 431))
        self.label.setStyleSheet("border-image: url(:/resource/images/Online Doctor-pana 2.svg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.diagnostic_page)
        self.label_4.setGeometry(QtCore.QRect(1240, 440, 31, 31))
        self.label_4.setStyleSheet("border-image: url(:/resource/images/loopa.svg);")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.diagnosis_button = QtWidgets.QPushButton(self.diagnostic_page)
        self.diagnosis_button.setGeometry(QtCore.QRect(870, 435, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.diagnosis_button.setFont(font)
        self.diagnosis_button.setStyleSheet("border-image: url(:/resource/images/selected_item.svg);\n"
"color: rgb(255, 255, 255);")
        self.diagnosis_button.setObjectName("diagnosis_button")
        self.frame_18 = QtWidgets.QFrame(self.diagnostic_page)
        self.frame_18.setGeometry(QtCore.QRect(0, 110, 51, 51))
        self.frame_18.setStyleSheet("border-image: url(:/resource/images/decor_2.svg);")
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.search_line.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.label_2.raise_()
        self.search_button.raise_()
        self.label_3.raise_()
        self.label.raise_()
        self.diagnosis_button.raise_()
        self.label_4.raise_()
        self.frame_18.raise_()
        self.stackedWidget.addWidget(self.diagnostic_page)
        self.post_diagnostic = QtWidgets.QWidget()
        self.post_diagnostic.setObjectName("post_diagnostic")
        self.label_5 = QtWidgets.QLabel(self.post_diagnostic)
        self.label_5.setGeometry(QtCore.QRect(30, 30, 821, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.selected_symptoms_frame_post_diagnostic = QtWidgets.QFrame(self.post_diagnostic)
        self.selected_symptoms_frame_post_diagnostic.setGeometry(QtCore.QRect(900, 70, 451, 501))
        self.selected_symptoms_frame_post_diagnostic.setStyleSheet("border-image: url(:/resource/images/Disease_about_bg.png);\n"
"")
        self.selected_symptoms_frame_post_diagnostic.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.selected_symptoms_frame_post_diagnostic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.selected_symptoms_frame_post_diagnostic.setObjectName("selected_symptoms_frame_post_diagnostic")
        self.selected_symptoms_list_postdiagnostic = QtWidgets.QListWidget(self.selected_symptoms_frame_post_diagnostic)
        self.selected_symptoms_list_postdiagnostic.setGeometry(QtCore.QRect(50, 40, 361, 411))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        font.setWeight(75)
        self.selected_symptoms_list_postdiagnostic.setFont(font)
        self.selected_symptoms_list_postdiagnostic.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                           \n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                             }\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                            border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;\n"
"                                            \n"
"                                            border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 2px 5px 0 5px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{\n"
"                                        background-color: rgb(87,194,163);\n"
"                                        border-radius: 10px;    \n"
"                                        padding:3px;\n"
"                                        color: rgb(255, 255, 255);\n"
"                                        margin:  5px 15px 0 0;\n"
"                                        }")
        self.selected_symptoms_list_postdiagnostic.setWordWrap(True)
        self.selected_symptoms_list_postdiagnostic.setObjectName("selected_symptoms_list_postdiagnostic")
        self.label_6 = QtWidgets.QLabel(self.post_diagnostic)
        self.label_6.setGeometry(QtCore.QRect(930, 30, 391, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.post_diagnostic)
        self.label_7.setGeometry(QtCore.QRect(20, 370, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.extra_symptoms_frame = QtWidgets.QFrame(self.post_diagnostic)
        self.extra_symptoms_frame.setGeometry(QtCore.QRect(0, 400, 401, 511))
        self.extra_symptoms_frame.setStyleSheet("border-image: url(:/resource/images/Disease_about_bg.png);\n"
"")
        self.extra_symptoms_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.extra_symptoms_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.extra_symptoms_frame.setObjectName("extra_symptoms_frame")
        self.extra_symptoms_list = QtWidgets.QListWidget(self.extra_symptoms_frame)
        self.extra_symptoms_list.setGeometry(QtCore.QRect(50, 50, 301, 411))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.extra_symptoms_list.setFont(font)
        self.extra_symptoms_list.setToolTipDuration(-1)
        self.extra_symptoms_list.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.extra_symptoms_list.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                         background-color:rgb(87,194,163);\n"
"                                                 color: rgb(112, 112, 112);\n"
"                                                 color: rgb(255, 255, 255);\n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                        color:rgb(87,194,163);}\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                        border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;    \n"
"                                        \n"
"                                        border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"\n"
"                                        margin: 2px 5px 0 0px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{    \n"
"                                        background-color: rgb(231, 231, 232);\n"
"                                        border-radius: 10px;\n"
"                                        color: rgb(112, 112, 112);\n"
"                                        margin:  5px 5px 0 0;\n"
"                                        padding: 3px;\n"
"                                        }")
        self.extra_symptoms_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.extra_symptoms_list.setDragEnabled(False)
        self.extra_symptoms_list.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.extra_symptoms_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.extra_symptoms_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.extra_symptoms_list.setTextElideMode(QtCore.Qt.ElideNone)
        self.extra_symptoms_list.setFlow(QtWidgets.QListView.TopToBottom)
        self.extra_symptoms_list.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.extra_symptoms_list.setUniformItemSizes(False)
        self.extra_symptoms_list.setWordWrap(True)
        self.extra_symptoms_list.setSelectionRectVisible(False)
        self.extra_symptoms_list.setObjectName("extra_symptoms_list")
        self.frame_9 = QtWidgets.QFrame(self.post_diagnostic)
        self.frame_9.setGeometry(QtCore.QRect(430, 460, 471, 481))
        self.frame_9.setStyleSheet("border-image: url(:/resource/images/postdiag_bg_image_central.svg);")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.third_disease_frame = QtWidgets.QFrame(self.post_diagnostic)
        self.third_disease_frame.setGeometry(QtCore.QRect(600, 70, 311, 251))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.third_disease_frame.sizePolicy().hasHeightForWidth())
        self.third_disease_frame.setSizePolicy(sizePolicy)
        self.third_disease_frame.setMinimumSize(QtCore.QSize(311, 251))
        self.third_disease_frame.setStyleSheet("border-image: url(:/resource/images/Disease_plate_bg_shadow.png);")
        self.third_disease_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.third_disease_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.third_disease_frame.setObjectName("third_disease_frame")
        self.third_disease_pbar = QtWidgets.QProgressBar(self.third_disease_frame)
        self.third_disease_pbar.setGeometry(QtCore.QRect(40, 180, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.third_disease_pbar.setFont(font)
        self.third_disease_pbar.setStyleSheet("QProgressBar{\n"
"color:black;}\n"
"QProgressBar:horizontal {\n"
"border-radius: 12px;\n"
"background-color: rgb(232, 232, 232);\n"
"padding: 1px;\n"
"text-align: center;\n"
"margin-right: 4px;\n"
"border: none;\n"
"    border-image: none;\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background-color: rgb(112,112,112);\n"
"border-radius: 12px;\n"
"}\n"
"")
        self.third_disease_pbar.setProperty("value", 50)
        self.third_disease_pbar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.third_disease_pbar.setTextVisible(True)
        self.third_disease_pbar.setOrientation(QtCore.Qt.Horizontal)
        self.third_disease_pbar.setInvertedAppearance(False)
        self.third_disease_pbar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.third_disease_pbar.setObjectName("third_disease_pbar")
        self.third_disease_name = QtWidgets.QLabel(self.third_disease_frame)
        self.third_disease_name.setGeometry(QtCore.QRect(50, 40, 111, 121))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.third_disease_name.setFont(font)
        self.third_disease_name.setStyleSheet("border-image: none;\n"
"color:black;")
        self.third_disease_name.setScaledContents(False)
        self.third_disease_name.setWordWrap(True)
        self.third_disease_name.setObjectName("third_disease_name")
        self.third_disease_button = QtWidgets.QPushButton(self.third_disease_frame)
        self.third_disease_button.setGeometry(QtCore.QRect(30, 30, 251, 191))
        self.third_disease_button.setStyleSheet("border-image: none;\n"
"border:none;\n"
"background-color:transparent;")
        self.third_disease_button.setText("")
        self.third_disease_button.setObjectName("third_disease_button")
        self.third_disease_icon_frame = QtWidgets.QFrame(self.third_disease_frame)
        self.third_disease_icon_frame.setGeometry(QtCore.QRect(170, 70, 101, 101))
        self.third_disease_icon_frame.setStyleSheet("border-image: url(:/resource/images/plate_icon3.svg);")
        self.third_disease_icon_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.third_disease_icon_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.third_disease_icon_frame.setObjectName("third_disease_icon_frame")
        self.third_disease_icon_frame.raise_()
        self.third_disease_pbar.raise_()
        self.third_disease_name.raise_()
        self.third_disease_button.raise_()
        self.second_disease_frame = QtWidgets.QFrame(self.post_diagnostic)
        self.second_disease_frame.setGeometry(QtCore.QRect(300, 70, 311, 251))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.second_disease_frame.sizePolicy().hasHeightForWidth())
        self.second_disease_frame.setSizePolicy(sizePolicy)
        self.second_disease_frame.setMinimumSize(QtCore.QSize(311, 251))
        self.second_disease_frame.setStyleSheet("border-image: url(:/resource/images/Disease_plate_bg_shadow.png);")
        self.second_disease_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.second_disease_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.second_disease_frame.setObjectName("second_disease_frame")
        self.second_disease_pbar = QtWidgets.QProgressBar(self.second_disease_frame)
        self.second_disease_pbar.setGeometry(QtCore.QRect(40, 180, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.second_disease_pbar.setFont(font)
        self.second_disease_pbar.setStyleSheet("QProgressBar{\n"
"color:black;}\n"
"QProgressBar:horizontal {\n"
"border-radius: 12px;\n"
"background-color: rgb(232, 232, 232);\n"
"padding: 1px;\n"
"text-align: center;\n"
"margin-right: 4px;\n"
"border: none;\n"
"    border-image: none;\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background-color: rgb(64, 123, 255);\n"
"border-radius: 12px;\n"
"}\n"
"")
        self.second_disease_pbar.setProperty("value", 50)
        self.second_disease_pbar.setTextVisible(True)
        self.second_disease_pbar.setOrientation(QtCore.Qt.Horizontal)
        self.second_disease_pbar.setInvertedAppearance(False)
        self.second_disease_pbar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.second_disease_pbar.setObjectName("second_disease_pbar")
        self.second_disease_name = QtWidgets.QLabel(self.second_disease_frame)
        self.second_disease_name.setGeometry(QtCore.QRect(50, 40, 111, 121))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.second_disease_name.setFont(font)
        self.second_disease_name.setStyleSheet("border-image: none;\n"
"color:black;")
        self.second_disease_name.setScaledContents(False)
        self.second_disease_name.setWordWrap(True)
        self.second_disease_name.setObjectName("second_disease_name")
        self.second_disease_icon_frame = QtWidgets.QFrame(self.second_disease_frame)
        self.second_disease_icon_frame.setGeometry(QtCore.QRect(170, 70, 101, 101))
        self.second_disease_icon_frame.setStyleSheet("border-image: url(:/resource/images/plate_icon2.svg);")
        self.second_disease_icon_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.second_disease_icon_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.second_disease_icon_frame.setObjectName("second_disease_icon_frame")
        self.second_disease_button = QtWidgets.QPushButton(self.second_disease_frame)
        self.second_disease_button.setGeometry(QtCore.QRect(30, 30, 251, 191))
        self.second_disease_button.setStyleSheet("border-image: none;\n"
"border: 0px;\n"
"background-color:transparent;")
        self.second_disease_button.setText("")
        self.second_disease_button.setObjectName("second_disease_button")
        self.first_disease_frame = QtWidgets.QFrame(self.post_diagnostic)
        self.first_disease_frame.setGeometry(QtCore.QRect(0, 70, 311, 251))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.first_disease_frame.sizePolicy().hasHeightForWidth())
        self.first_disease_frame.setSizePolicy(sizePolicy)
        self.first_disease_frame.setMinimumSize(QtCore.QSize(311, 251))
        self.first_disease_frame.setStyleSheet("border-image: url(:/resource/images/Disease_plate_bg_shadow.png);")
        self.first_disease_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.first_disease_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.first_disease_frame.setObjectName("first_disease_frame")
        self.first_disease_pbar = QtWidgets.QProgressBar(self.first_disease_frame)
        self.first_disease_pbar.setGeometry(QtCore.QRect(40, 180, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_disease_pbar.setFont(font)
        self.first_disease_pbar.setStyleSheet("QProgressBar{\n"
"color:black;}\n"
"QProgressBar:horizontal {\n"
"border-radius: 12px;\n"
"background-color: rgb(232, 232, 232);\n"
"padding: 1px;\n"
"text-align: center;\n"
"margin-right: 4px;\n"
"border: none;\n"
"    border-image: none;\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background-color: rgb(87, 194, 162);\n"
"border-radius: 12px;\n"
"}\n"
"")
        self.first_disease_pbar.setProperty("value", 50)
        self.first_disease_pbar.setTextVisible(True)
        self.first_disease_pbar.setOrientation(QtCore.Qt.Horizontal)
        self.first_disease_pbar.setInvertedAppearance(False)
        self.first_disease_pbar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.first_disease_pbar.setObjectName("first_disease_pbar")
        self.first_disease_name = QtWidgets.QLabel(self.first_disease_frame)
        self.first_disease_name.setGeometry(QtCore.QRect(50, 40, 111, 121))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_disease_name.setFont(font)
        self.first_disease_name.setStyleSheet("border-image: none;\n"
"color:black;")
        self.first_disease_name.setScaledContents(False)
        self.first_disease_name.setWordWrap(True)
        self.first_disease_name.setObjectName("first_disease_name")
        self.first_disease_icon_frame = QtWidgets.QFrame(self.first_disease_frame)
        self.first_disease_icon_frame.setGeometry(QtCore.QRect(170, 70, 101, 101))
        self.first_disease_icon_frame.setStyleSheet("border-image: url(:/resource/images/plate_icon1.svg);")
        self.first_disease_icon_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.first_disease_icon_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.first_disease_icon_frame.setObjectName("first_disease_icon_frame")
        self.first_disease_button = QtWidgets.QPushButton(self.first_disease_frame)
        self.first_disease_button.setGeometry(QtCore.QRect(30, 30, 251, 191))
        self.first_disease_button.setStyleSheet("border-image: none;\n"
"border:none;\n"
"background-color:transparent;")
        self.first_disease_button.setText("")
        self.first_disease_button.setObjectName("first_disease_button")
        self.recalculation_button = QtWidgets.QPushButton(self.post_diagnostic)
        self.recalculation_button.setGeometry(QtCore.QRect(920, 570, 411, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.recalculation_button.setFont(font)
        self.recalculation_button.setStyleSheet("border-image: url(:/resource/images/selected_item.svg);\n"
"color: rgb(255, 255, 255);")
        self.recalculation_button.setObjectName("recalculation_button")
        self.label_8 = QtWidgets.QLabel(self.post_diagnostic)
        self.label_8.setGeometry(QtCore.QRect(1290, 570, 41, 41))
        self.label_8.setStyleSheet("border-image: url(:/resource/images/Reset_Button.svg);")
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.update_symptoms_button = QtWidgets.QPushButton(self.post_diagnostic)
        self.update_symptoms_button.setGeometry(QtCore.QRect(410, 365, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.update_symptoms_button.setFont(font)
        self.update_symptoms_button.setStyleSheet("QPushButton{\n"
"border-image: url(:/resource/images/Plus_button.svg);\n"
"}\n"
"QPushButton:hover{\n"
"border-image: url(:/resource/images/Plus_button_hover.svg);\n"
"}")
        self.update_symptoms_button.setText("")
        self.update_symptoms_button.setObjectName("update_symptoms_button")
        self.label_13 = QtWidgets.QLabel(self.post_diagnostic)
        self.label_13.setGeometry(QtCore.QRect(430, 370, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-image: none;\n"
"border:none;\n"
"border-radius: 20px;\n"
"padding-left: 40px;")
        self.label_13.setObjectName("label_13")
        self.label_13.raise_()
        self.label_5.raise_()
        self.selected_symptoms_frame_post_diagnostic.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.extra_symptoms_frame.raise_()
        self.frame_9.raise_()
        self.third_disease_frame.raise_()
        self.second_disease_frame.raise_()
        self.first_disease_frame.raise_()
        self.recalculation_button.raise_()
        self.update_symptoms_button.raise_()
        self.label_8.raise_()
        self.stackedWidget.addWidget(self.post_diagnostic)
        self.disease_info_page = QtWidgets.QWidget()
        self.disease_info_page.setObjectName("disease_info_page")
        self.label_9 = QtWidgets.QLabel(self.disease_info_page)
        self.label_9.setGeometry(QtCore.QRect(70, 30, 491, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.disease_info_page)
        self.label_10.setGeometry(QtCore.QRect(780, 130, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_10.setObjectName("label_10")
        self.all_symptoms_disease_frame = QtWidgets.QFrame(self.disease_info_page)
        self.all_symptoms_disease_frame.setGeometry(QtCore.QRect(740, 160, 591, 501))
        self.all_symptoms_disease_frame.setStyleSheet("border-image: url(:/resource/images/Disease_about_bg.png);\n"
"")
        self.all_symptoms_disease_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.all_symptoms_disease_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.all_symptoms_disease_frame.setObjectName("all_symptoms_disease_frame")
        self.all_symptoms_disease_listwidget = QtWidgets.QListWidget(self.all_symptoms_disease_frame)
        self.all_symptoms_disease_listwidget.setGeometry(QtCore.QRect(60, 50, 481, 401))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.all_symptoms_disease_listwidget.setFont(font)
        self.all_symptoms_disease_listwidget.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                           \n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                             }\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                            border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;\n"
"                                            \n"
"                                            border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"                                        boder-radius:0px;\n"
"                                        margin: 2px 5px 0 5px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{\n"
"                                        background-color: rgb(87,194,163);\n"
"                                        border-radius: 10px;    \n"
"                                        padding:3px;\n"
"                                        color: rgb(255, 255, 255);\n"
"                                        margin:  5px 15px 0 0;\n"
"                                        }")
        self.all_symptoms_disease_listwidget.setObjectName("all_symptoms_disease_listwidget")
        self.label_11 = QtWidgets.QLabel(self.disease_info_page)
        self.label_11.setGeometry(QtCore.QRect(700, 30, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(112, 112, 112);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_11.setObjectName("label_11")
        self.disease_info_frame = QtWidgets.QFrame(self.disease_info_page)
        self.disease_info_frame.setGeometry(QtCore.QRect(30, 80, 691, 771))
        self.disease_info_frame.setStyleSheet("border-image: url(:/resource/images/Disease_about_bg.png);")
        self.disease_info_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.disease_info_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.disease_info_frame.setObjectName("disease_info_frame")
        self.disease_info_text_browser = QtWidgets.QTextBrowser(self.disease_info_frame)
        self.disease_info_text_browser.setGeometry(QtCore.QRect(60, 70, 571, 631))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.disease_info_text_browser.setFont(font)
        self.disease_info_text_browser.setStyleSheet("QTextBrowser{\n"
"border-image:none;\n"
"background-color:white;\n"
"border: none;\n"
"color:black;\n"
"border-radius:15px\n"
" }\n"
"QScrollBar:vertical {\n"
" boder:none;\n"
"border-image: url(:/resource/images/scroll_bg.png);\n"
"margin: 5px 0 5px 0;}")
        self.disease_info_text_browser.setObjectName("disease_info_text_browser")
        self.disease_type_label = QtWidgets.QLabel(self.disease_info_page)
        self.disease_type_label.setGeometry(QtCore.QRect(960, 30, 331, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.disease_type_label.setFont(font)
        self.disease_type_label.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(87,194,163);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.disease_type_label.setObjectName("disease_type_label")
        self.return_button = QtWidgets.QPushButton(self.disease_info_page)
        self.return_button.setGeometry(QtCore.QRect(1030, 660, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.return_button.setFont(font)
        self.return_button.setStyleSheet("border-image: none;\n"
"border-radius: 20px;\n"
"background-color: rgb(87,194,163);\n"
"color: rgb(255, 255, 255);")
        self.return_button.setObjectName("return_button")
        self.stackedWidget.addWidget(self.disease_info_page)
        self.house_page = QtWidgets.QWidget()
        self.house_page.setObjectName("house_page")
        self.frame_4 = QtWidgets.QFrame(self.house_page)
        self.frame_4.setGeometry(QtCore.QRect(-20, 10, 451, 431))
        self.frame_4.setStyleSheet("border-image: url(:/resource/images/house_page_plate.png);\n"
"border:none;")

        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")





        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setGeometry(QtCore.QRect(50, 130, 221, 221))
        self.frame_5.setStyleSheet("border-image: url(:/resource/images/house_page_plate_image1.svg);\n"
"border:none;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")

        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setGeometry(QtCore.QRect(60, 30, 61, 61))
        self.frame_6.setStyleSheet("border-image: url(:/resource/images/search_image.svg);\n"
"border:none;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.label_15 = QtWidgets.QLabel(self.frame_4)
        self.label_15.setGeometry(QtCore.QRect(150, 30, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("border-image: none;\n"
"border:none;")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setGeometry(QtCore.QRect(150, 70, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("border-image: none;\n"
"border:none;\n"
"color: rgb(162, 162, 162);")
        self.label_16.setWordWrap(True)
        self.label_16.setObjectName("label_16")

        self.frame_4_button = QtWidgets.QPushButton(self.frame_4)
        self.frame_4_button.setGeometry(QtCore.QRect(-30, -20, 371, 341))
        self.frame_4_button.setStyleSheet("border-image: none;\n")
        self.frame_4_button.raise_()
        self.frame_4_button.clicked.connect(self.move_to_diagnostics)

        self.frame_7 = QtWidgets.QFrame(self.house_page)
        self.frame_7.setGeometry(QtCore.QRect(400, 20, 251, 231))
        self.frame_7.setStyleSheet("border-image: url(:/resource/images/house_page_plate.png);\n"
"border:none;")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")





        self.frame_13 = QtWidgets.QFrame(self.frame_7)
        self.frame_13.setGeometry(QtCore.QRect(30, 20, 71, 71))
        self.frame_13.setStyleSheet("border-image: url(:/resource/images/plate_icon4.svg);\n"
"border:none;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.label_28 = QtWidgets.QLabel(self.frame_7)
        self.label_28.setGeometry(QtCore.QRect(30, 90, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("border-image: none;\n"
"border:none;")
        self.label_28.setObjectName("label_28")
        self.label_27 = QtWidgets.QLabel(self.frame_7)
        self.label_27.setGeometry(QtCore.QRect(30, 130, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("border-image: none;\n"
"border:none;\n"
"color: rgb(162, 162, 162);")
        self.label_27.setWordWrap(True)
        self.label_27.setObjectName("label_27")

        self.frame_7_button = QtWidgets.QPushButton(self.frame_7)
        self.frame_7_button.setGeometry(QtCore.QRect(-10, -10, 201, 181))
        self.frame_7_button.setStyleSheet("border-image: none;\n")
        self.frame_7_button.raise_()
        self.frame_7_button.clicked.connect(self.in_development)


        self.frame_8 = QtWidgets.QFrame(self.house_page)
        self.frame_8.setGeometry(QtCore.QRect(640, 20, 251, 231))
        self.frame_8.setStyleSheet("border-image: url(:/resource/images/house_page_plate.png);\n"
"border:none;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.frame_14 = QtWidgets.QFrame(self.frame_8)
        self.frame_14.setGeometry(QtCore.QRect(30, 20, 61, 61))
        self.frame_14.setStyleSheet("border-image: url(:/resource/images/plate_icon6.svg);\n"
"border:none;")
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.label_30 = QtWidgets.QLabel(self.frame_8)
        self.label_30.setGeometry(QtCore.QRect(30, 90, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("border-image: none;\n"
"border:none;")
        self.label_30.setObjectName("label_30")
        self.label_29 = QtWidgets.QLabel(self.frame_8)
        self.label_29.setGeometry(QtCore.QRect(30, 130, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("border-image: none;\n"
"border:none;\n"
"color: rgb(162, 162, 162);")
        self.label_29.setWordWrap(True)
        self.label_29.setObjectName("label_29")

        self.frame_8_button = QtWidgets.QPushButton(self.frame_8)
        self.frame_8_button.setGeometry(QtCore.QRect(20, 10, 201, 181))
        self.frame_8_button.setStyleSheet("border-image: none;\n")
        self.frame_8_button.raise_()
        self.frame_8_button.clicked.connect(self.move_to_doctors)






        self.frame_10 = QtWidgets.QFrame(self.house_page)
        self.frame_10.setGeometry(QtCore.QRect(880, 20, 251, 231))
        self.frame_10.setStyleSheet("border-image: url(:/resource/images/house_page_plate.png);\n"
"border:none;")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.frame_15 = QtWidgets.QFrame(self.frame_10)
        self.frame_15.setGeometry(QtCore.QRect(40, 20, 51, 61))
        self.frame_15.setStyleSheet("border-image: url(:/resource/images/plate_icon5.svg);\n"
"border:none;")
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.label_32 = QtWidgets.QLabel(self.frame_10)
        self.label_32.setGeometry(QtCore.QRect(30, 90, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("border-image: none;\n"
"border:none;")
        self.label_32.setObjectName("label_32")
        self.label_31 = QtWidgets.QLabel(self.frame_10)
        self.label_31.setGeometry(QtCore.QRect(30, 130, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("border-image: none;\n"
"border:none;\n"
"color: rgb(162, 162, 162);")
        self.label_31.setWordWrap(True)
        self.label_31.setObjectName("label_31")
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.frame_12 = QtWidgets.QFrame(self.house_page)
        self.frame_12.setGeometry(QtCore.QRect(-20, 410, 741, 481))
        self.frame_12.setStyleSheet("border-image: url(:/resource/images/stat_bg.svg);")
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.label_17 = QtWidgets.QLabel(self.frame_12)
        self.label_17.setGeometry(QtCore.QRect(440, 50, 31, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("border-image:none;")
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.frame_12)
        self.label_18.setGeometry(QtCore.QRect(440, 120, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("border-image:none;")
        self.label_18.setObjectName("label_18")

        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_20 = QtWidgets.QLabel(self.frame_12)
        self.label_20.setGeometry(QtCore.QRect(520, 120, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("border-image:none;")
        self.label_20.setText("")
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.frame_12)
        self.label_21.setGeometry(QtCore.QRect(520, 50, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("border-image:none;")
        self.label_21.setText("")
        self.label_21.setObjectName("label_21")
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_23 = QtWidgets.QLabel(self.frame_12)
        self.label_23.setGeometry(QtCore.QRect(270, 195, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("border-image:none;\n"
"color: rgb(255, 255, 255);")
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.frame_12)
        self.label_24.setGeometry(QtCore.QRect(270, 410, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("border-image:none;\n"
"color: rgb(255, 255, 255);")
        self.label_24.setObjectName("label_24")

        self.frame_10_button = QtWidgets.QPushButton(self.frame_10)
        self.frame_10_button.setGeometry(QtCore.QRect(20, 10, 201, 181))
        self.frame_10_button.setStyleSheet("border-image: none;\n")
        self.frame_10_button.raise_()
        self.frame_10_button.clicked.connect(self.in_development)

        self.label_25 = QtWidgets.QLabel(self.frame_12)
        self.label_25.setGeometry(QtCore.QRect(270, 255, 341, 31))
        self.label_25.setStyleSheet("border-image:none;")
        self.label_25.setText("")
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.frame_12)
        self.label_26.setGeometry(QtCore.QRect(270, 320, 341, 31))
        self.label_26.setStyleSheet("border-image:none;")
        self.label_26.setText("")
        self.label_26.setObjectName("label_26")
        self.label_26.setFont(font)
        self.frame_19 = QtWidgets.QFrame(self.house_page)
        self.frame_19.setGeometry(QtCore.QRect(630, 390, 81, 80))
        self.frame_19.setStyleSheet("border-image: url(:/resource/images/decor_6.svg);")
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.frame_21 = QtWidgets.QFrame(self.house_page)
        self.frame_21.setGeometry(QtCore.QRect(450, 260, 191, 111))
        self.frame_21.setStyleSheet("border-image: url(:/resource/images/decor_8.svg);")
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.frame_19.raise_()
        self.frame_4.raise_()
        self.frame_7.raise_()
        self.frame_8.raise_()
        self.frame_10.raise_()
        self.frame_12.raise_()
        self.frame_21.raise_()
        self.stackedWidget.addWidget(self.house_page)
        self.statistics_page = QtWidgets.QWidget()
        self.statistics_page.setObjectName("statistics_page")
        self.stackedWidget.addWidget(self.statistics_page)
        self.doctors_page = QtWidgets.QWidget()
        self.doctors_page.setObjectName("doctors_page")
        self.frame_20 = QtWidgets.QFrame(self.doctors_page)
        self.frame_20.setGeometry(QtCore.QRect(10, 100, 971, 461))
        self.frame_20.setStyleSheet("border-image: url(:/resource/images/docto_info_bg.png);")
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.frame_25 = QtWidgets.QFrame(self.frame_20)
        self.frame_25.setGeometry(QtCore.QRect(70, 40, 161, 211))
        self.frame_25.setStyleSheet("border-image: url(:/resource/images/doctor_example.png);")
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.Name_1 = QtWidgets.QLabel(self.frame_20)
        self.Name_1.setGeometry(QtCore.QRect(70, 270, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Name_1.setFont(font)
        self.Name_1.setStyleSheet("border-image: none;")
        self.Name_1.setAlignment(QtCore.Qt.AlignCenter)
        self.Name_1.setObjectName("Name_1")
        self.Education_1 = QtWidgets.QLabel(self.frame_20)
        self.Education_1.setGeometry(QtCore.QRect(260, 90, 611, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Education_1.setFont(font)
        self.Education_1.setStyleSheet("border-image: none;"
                                       "color:black")
        self.Education_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Education_1.setWordWrap(True)
        self.Education_1.setObjectName("Education_1")
        self.Doctor_1_Category_1 = QtWidgets.QLabel(self.frame_20)
        self.Doctor_1_Category_1.setGeometry(QtCore.QRect(260, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_1_Category_1.setFont(font)
        self.Doctor_1_Category_1.setStyleSheet("border-image: none;\n"
                                      "color:black;"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_1_Category_1.setScaledContents(False)
        self.Doctor_1_Category_1.setWordWrap(False)
        self.Doctor_1_Category_1.setObjectName("Doctor_1_Category_1")
        self.Doctor_1_Category_2 = QtWidgets.QLabel(self.frame_20)
        self.Doctor_1_Category_2.setGeometry(QtCore.QRect(460, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_1_Category_2.setFont(font)
        self.Doctor_1_Category_2.setStyleSheet("border-image: none;\n"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_1_Category_2.setObjectName("Doctor_1_Category_2")
        self.Doctor_1_Category_3 = QtWidgets.QLabel(self.frame_20)
        self.Doctor_1_Category_3.setGeometry(QtCore.QRect(660, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_1_Category_3.setFont(font)
        self.Doctor_1_Category_3.setStyleSheet("border-image: none;\n"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_1_Category_3.setObjectName("Doctor_1_Category_3")
        self.Doctor_1_Experience = QtWidgets.QLabel(self.frame_20)
        self.Doctor_1_Experience.setGeometry(QtCore.QRect(260, 130, 611, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_1_Experience.setFont(font)
        self.Doctor_1_Experience.setStyleSheet("border-image: none;"
                                    "color:black;")
        self.Doctor_1_Experience.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Doctor_1_Experience.setWordWrap(True)
        self.Doctor_1_Experience.setObjectName("Doctor_1_Experience")
        self.Doctor_1_Description = QtWidgets.QLabel(self.frame_20)
        self.Doctor_1_Description.setGeometry(QtCore.QRect(260, 180, 611, 111))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_1_Description.setFont(font)
        self.Doctor_1_Description.setStyleSheet("border-image: none;"
                                    "color:black;")
        self.Doctor_1_Description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Doctor_1_Description.setWordWrap(True)
        self.Doctor_1_Description.setObjectName("Doctor_1_Description")
        self.contact_button_1 = QtWidgets.QPushButton(self.frame_20)

        self.contact_button_1.setGeometry(QtCore.QRect(70, 310, 811, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.contact_button_1.setFont(font)
        self.contact_button_1.setStyleSheet("background-color: rgb(87, 194, 162);\n"
"border-image:none;\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.contact_button_1.setObjectName("contact_button_1")
        self.search_line_2 = QtWidgets.QLineEdit(self.doctors_page)
        self.search_line_2.setGeometry(QtCore.QRect(50, 30, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setBold(True)
        font.setWeight(75)
        self.search_line_2.setFont(font)
        self.search_line_2.setStyleSheet("border-image: url(:/resource/images/search_bg.svg);\n"
"color: rgb(97, 97, 97);\n"
"padding-left:15px")
        self.search_line_2.setText("")

        self.search_line_2.setObjectName("search_line_2")
        self.search_button_2 = QtWidgets.QPushButton(self.doctors_page)
        self.search_button_2.setGeometry(QtCore.QRect(570, 30, 41, 41))
        self.search_button_2.setStyleSheet("QPushButton{\n"
"    border-image: url(:/resource/images/searchbutton.svg);}\n"
"QPushButton:hover{\n"
"    border-image: url(:/resource/images/searchbutton_hover.svg);\n"
"}")
        self.search_button_2.setText("")
        self.search_button_2.setObjectName("search_button_2")
        self.frame_23 = QtWidgets.QFrame(self.doctors_page)
        self.frame_23.setGeometry(QtCore.QRect(940, 70, 411, 621))
        self.frame_23.setStyleSheet("border-image: url(:/resource/images/list_bg.png);\n"
"")
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.symptoms_list_2 = QtWidgets.QListWidget(self.frame_23)
        self.symptoms_list_2.setGeometry(QtCore.QRect(50, 60, 321, 371))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.symptoms_list_2.setFont(font)
        self.symptoms_list_2.setToolTipDuration(-1)
        self.symptoms_list_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.symptoms_list_2.setStyleSheet("QListView{\n"
"                                        outline:0;\n"
"                                        }\n"
"                                        QListWidget{\n"
"                                        border-image:none;\n"
"                                        border:none;    \n"
"                                            background-color:white\n"
"                                        }\n"
"                                        QListView::item:selected {\n"
"                                         background-color:rgb(87,194,163);\n"
"                                                 color: rgb(112, 112, 112);\n"
"                                                 color: rgb(255, 255, 255);\n"
"                                        }\n"
"                                        QListView::item::hover{\n"
"                                        color:rgb(87,194,163);}\n"
"                                        QScrollBar:vertical {\n"
"                                        boder:none;\n"
"                                        border-image: url(:/resource/images/scroll_bg.png);\n"
"                                        margin: 5px 0 5px 0;\n"
"                                        }\n"
"                                            QScrollBar:horizontal {\n"
"                                        boder:none;    \n"
"                                        \n"
"                                        border-image: url(:/resource/images/horizontal_scroll_bg.png);\n"
"\n"
"                                        margin: 2px 5px 0 0px;\n"
"                                        }\n"
"                                        QListView::item:selected::hover{\n"
"                                        color:rgb(255,255,255)}\n"
"                                        QListView::item{    \n"
"                                        background-color: rgb(231, 231, 232);\n"
"                                        border-radius: 10px;\n"
"                                        color: rgb(112, 112, 112);\n"
"                                        margin:  5px 10px 0 0;\n"
"                                        padding:3px;\n"
"                                        }")
        self.symptoms_list_2.setDragEnabled(True)
        self.symptoms_list_2.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.symptoms_list_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.symptoms_list_2.setTextElideMode(QtCore.Qt.ElideNone)
        self.symptoms_list_2.setFlow(QtWidgets.QListView.TopToBottom)
        self.symptoms_list_2.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.symptoms_list_2.setUniformItemSizes(False)
        self.symptoms_list_2.setWordWrap(True)
        self.symptoms_list_2.setSelectionRectVisible(False)
        self.symptoms_list_2.setObjectName("symptoms_list_2")
        self.frame_24 = QtWidgets.QFrame(self.frame_23)
        self.frame_24.setGeometry(QtCore.QRect(310, 520, 101, 91))
        self.frame_24.setStyleSheet("border-image: url(:/resource/images/decor_3.svg);")
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.label_12 = QtWidgets.QLabel(self.doctors_page)
        self.label_12.setGeometry(QtCore.QRect(970, 60, 351, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("border-image: none;\n"
"border-radius: 15px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:8px;\n"
"color: rgb(255, 255, 255);")
        self.label_12.setObjectName("label_12")
        self.frame_22 = QtWidgets.QFrame(self.doctors_page)
        self.frame_22.setGeometry(QtCore.QRect(10, 510, 971, 461))
        self.frame_22.setStyleSheet("border-image: url(:/resource/images/docto_info_bg.png);")
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.frame_26 = QtWidgets.QFrame(self.frame_22)
        self.frame_26.setGeometry(QtCore.QRect(70, 40, 161, 211))
        self.frame_26.setStyleSheet("border-image: url(:/resource/images/doctor_example_2.jpg);")
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.Doctor_2_Name = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Name.setGeometry(QtCore.QRect(70, 270, 161, 20))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Name.setFont(font)
        self.Doctor_2_Name.setStyleSheet("border-image: none;")
        self.Doctor_2_Name.setAlignment(QtCore.Qt.AlignCenter)
        self.Doctor_2_Name.setObjectName("Doctor_2_Name")
        self.Doctor_2_Education = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Education.setGeometry(QtCore.QRect(260, 90, 611, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Education.setFont(font)
        self.Doctor_2_Education.setStyleSheet("border-image: none;"
                                              "color:black;")
        self.Doctor_2_Education.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Doctor_2_Education.setWordWrap(True)
        self.Doctor_2_Education.setObjectName("Doctor_2_Education")
        self.Doctor_2_Category_1 = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Category_1.setGeometry(QtCore.QRect(260, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Category_1.setFont(font)
        self.Doctor_2_Category_1.setStyleSheet("border-image: none;\n"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_2_Category_1.setScaledContents(False)
        self.Doctor_2_Category_1.setWordWrap(False)
        self.Doctor_2_Category_1.setObjectName("Doctor_2_Category_1")
        self.Doctor_2_Category_2 = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Category_2.setGeometry(QtCore.QRect(460, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Category_2.setFont(font)
        self.Doctor_2_Category_2.setStyleSheet("border-image: none;\n"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_2_Category_2.setObjectName("Doctor_2_Category_2")
        self.Doctor_2_Category_3 = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Category_3.setGeometry(QtCore.QRect(660, 40, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Category_3.setFont(font)
        self.Doctor_2_Category_3.setStyleSheet("border-image: none;\n"
"border-radius: 10px;\n"
"background-color: rgb(87, 194, 162);\n"
"padding-left:5px;\n"
"color: rgb(255, 255, 255);")
        self.Doctor_2_Category_3.setObjectName("Doctor_2_Category_3")
        self.Doctor_2_Experience = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Experience.setGeometry(QtCore.QRect(260, 130, 611, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Experience.setFont(font)
        self.Doctor_2_Experience.setStyleSheet("border-image: none;"
                                               "color:black;")
        self.Doctor_2_Experience.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Doctor_2_Experience.setWordWrap(True)
        self.Doctor_2_Experience.setObjectName("Doctor_2_Experience")
        self.Doctor_2_Description = QtWidgets.QLabel(self.frame_22)
        self.Doctor_2_Description.setGeometry(QtCore.QRect(260, 180, 611, 111))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Doctor_2_Description.setFont(font)
        self.Doctor_2_Description.setStyleSheet("border-image: none;"
                                                "color:black;")
        self.Doctor_2_Description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Doctor_2_Description.setWordWrap(True)
        self.Doctor_2_Description.setObjectName("Doctor_2_Description")
        self.contact_button_2 = QtWidgets.QPushButton(self.frame_22)
        self.contact_button_2.setGeometry(QtCore.QRect(70, 310, 811, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.contact_button_2.setFont(font)
        self.contact_button_2.setStyleSheet("background-color: rgb(87, 194, 162);\n"
"border-image:none;\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);")
        self.contact_button_2.setObjectName("contact_button_2")
        self.stackedWidget.addWidget(self.doctors_page)
        self.my_acc_page = QtWidgets.QWidget()
        self.my_acc_page.setObjectName("my_acc_page")
        self.frame_16 = QtWidgets.QFrame(self.post_diagnostic)
        self.frame_16.setGeometry(QtCore.QRect(900, 590, 461, 311))
        self.frame_16.setStyleSheet("border:none;\n"
                                    "border-image: url(:/resource/images/white_rectangle.png);")
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.recommended_label = QtWidgets.QLabel(self.frame_16)
        self.recommended_label.setGeometry(QtCore.QRect(50, 45, 371, 22))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recommended_label.setFont(font)
        self.recommended_label.setStyleSheet("border:none;\n"
                                             "border-image:none;\n"
                                             "color:black;")
        self.recommended_label.setObjectName("recommended_label")
        self.recommended_doctor_image = QtWidgets.QLabel(self.frame_16)
        self.recommended_doctor_image.setGeometry(QtCore.QRect(50, 80, 131, 171))
        self.recommended_doctor_image.setStyleSheet("border-image:none;")
        self.recommended_doctor_image.setText("")
        self.recommended_doctor_image.setObjectName("recommended_doctor_image")
        self.recommended_name = QtWidgets.QLabel(self.frame_16)
        self.recommended_name.setGeometry(QtCore.QRect(200, 90, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recommended_name.setFont(font)
        self.recommended_name.setStyleSheet("border-image:none;\n"
                                            "color:black;")
        self.recommended_name.setObjectName("recommended_name")
        self.recommended_experience = QtWidgets.QLabel(self.frame_16)
        self.recommended_experience.setGeometry(QtCore.QRect(200, 140, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recommended_experience.setFont(font)
        self.recommended_experience.setStyleSheet("border-image:none;\n"
                                                  "color:black;")
        self.recommended_experience.setObjectName("recommended_experience")
        self.recommended_button = QtWidgets.QPushButton(self.frame_16)
        self.recommended_button.setGeometry(QtCore.QRect(190, 210, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.recommended_button.setFont(font)
        self.recommended_button.setStyleSheet("border-image:none;\n"
                                              "background-color: rgb(87, 194, 162);\n"
                                              "border-radius:19px;")
        self.recommended_button.setObjectName("recommended_button")
        self.stackedWidget.addWidget(self.my_acc_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        ########CODE
        self.statictics_page_button.clicked.connect(self.in_development)
        self.house_page_button.clicked.connect(self.move_to_house)
        self.diagnostics_page_button.clicked.connect(self.move_to_diagnostics)
        self.doctors_page_button.clicked.connect(self.move_to_doctors)
        self.recalculation_button.clicked.connect(self.recalculation)
        self.recommended_button.clicked.connect(self.move_to_doctors_from_diagnostics)
        all_symptoms = set()
        for obj in gc.get_objects():
                if isinstance(obj, Disease):
                        for symptom in obj.symptoms:
                                all_symptoms.add(str(symptom))
        all_symptoms = (list(all_symptoms))
        all_symptoms.sort()
        self.symptoms_list.itemDoubleClicked.connect(self.move_symptom)
        self.selected_symptoms_list.itemDoubleClicked.connect(self.delete_symptom)
        self.search_button.clicked.connect(self.search_symptom)
        self.diagnosis_button.clicked.connect(self.diagnosis_run)
        self.update_symptoms_button.clicked.connect(self.update_symptoms)
        self.return_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        completer = QtWidgets.QCompleter()
        self.search_line.setCompleter(completer)
        model = QtCore.QStringListModel()
        completer.setModel(model)
        delegate = CompleterDelegate(self.search_line)
        completer.popup().setItemDelegate(delegate)
        completer.popup().setFont(font)
        completer.popup().setStyleSheet("QAbstractItemView{"
                                        "border-image:none;"
                                        "border: none;"
                                        "padding: 1px;"
                                        "color: rgb(112,112,112);"
                                        "border-radius: 15px;}"
                                        "QAbstractItemView::item:hover{"
                                        "color: rgb(87,194,163)"
                                        "}\n"
                                        "QScrollBar:vertical {\n"
                                        "                                 boder:none;\n"
                                        "                                 border-image: url(:/resource/images/scroll_bg.png);\n"
                                        "                                 margin: 0 0 0 0;\n"
                                        "                                 boder-radius:0px;\n"
                                        "                                 }\n"
                                        "                                 QScrollBar::handle:vertical {\n"
                                        "                                 background-color: rgb(0, 170, 127);\n"
                                        "                                 border-radius: 8px;\n"
                                        "                                 }\n"
                                        "                                  QScrollBar::add-line:vertical {\n"
                                        "                                      border: none;\n"
                                        "                                      \n"
                                        "                                     \n"
                                        "                                  }\n"
                                        "                                 QScrollBar::sub-line:vertical {\n"
                                        "                                      border: none;\n"
                                        "                                     \n"
                                        "                                  }\n"
                                        "                                 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                        "                                      background: none;\n"
                                        "                                    \n"
                                        "                                 }\n"
                                        "                                  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                        "                                      background: none;\n"
                                        "                                  }\n"
                                        "\n"
                                        "}")
        self.get_data(model)
        for i in range(len(all_symptoms)):
                item = QtWidgets.QListWidgetItem()
                self.symptoms_list.addItem(item)
        for i in range(len(all_symptoms)):
                item = self.symptoms_list.item(i)
                item.setText(all_symptoms[i])
        #########
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        self.contact_button_1.clicked.connect(lambda : webbrowser.open("https://t.me/+0qIQGr79ekYxOTQ6"))
        self.contact_button_2.clicked.connect(lambda : webbrowser.open("https://t.me/som1c"))

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_line.setPlaceholderText(_translate("MainWindow", "Пошук симптомів"))
        self.symptoms_list.setToolTip(_translate("MainWindow", "Кашель"))
        self.symptoms_list.setSortingEnabled(False)
        self.label_2.setText(_translate("MainWindow", "Обрані симптоми"))
        self.label_3.setText(_translate("MainWindow", "Оберіть симптоми"))
        self.diagnosis_button.setText(_translate("MainWindow", "Перевірка"))
        self.label_5.setText(_translate("MainWindow", "Можливі захворювання"))
        self.label_6.setText(_translate("MainWindow", "Вибрані симптоми"))
        self.label_7.setText(_translate("MainWindow", "Оберіть додаткові симптоми"))
        self.extra_symptoms_list.setSortingEnabled(False)
        self.third_disease_name.setText(_translate("MainWindow", "Захворювання нирок та застій жовчі"))
        self.second_disease_name.setText(_translate("MainWindow", "Захворювання нирок та застій жовчі"))
        self.first_disease_name.setText(_translate("MainWindow", "Захворювання нирок та застій жовчі"))
        self.recalculation_button.setText(_translate("MainWindow", "Перерахунок"))
        self.label_13.setText(_translate("MainWindow", "Оновити симптоми"))
        self.label_9.setText(_translate("MainWindow", "Інформація про захворювання"))
        self.label_10.setText(_translate("MainWindow", "Всі симптоми захворювання"))
        self.label_11.setText(_translate("MainWindow", "Тип захворювання:"))
        self.disease_info_text_browser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.зфщцуофцущаєфзщцуопзмщєіузкщпоєфзщофузщппфукпфущкофзщукпозєщфсфєзщукпофзщоєфузщкпофєущкпфкпфк.пфкщпофєщофузщкопщзфопєфзщукєфзщукопфпфукп.фвапзщфоєузщкпоєвфдамьєзщукпфв.апфущкопфзщпдфука.</p></body></html>"))
        self.disease_type_label.setText(_translate("MainWindow", "Студентське захворювання"))
        self.return_button.setText(_translate("MainWindow", "Повернутись"))
        self.label_15.setText(_translate("MainWindow", "Визначити хворобу"))
        self.label_16.setText(_translate("MainWindow", "Виберіть симптоми, що вас турбують та отримайте ймовірний діагноз"))
        self.label_28.setText(_translate("MainWindow", "Усі хвороби"))
        self.label_27.setText(_translate("MainWindow", "Виберіть симптоми, що вас турбують та отримайте ймовірний діагноз"))
        self.label_30.setText(_translate("MainWindow", "Знайти лікаря"))
        self.label_29.setText(_translate("MainWindow", "Виберіть симптоми, що вас турбують та отримайте ймовірний діагноз"))
        self.label_32.setText(_translate("MainWindow", "Історія хворіб"))
        self.label_31.setText(_translate("MainWindow", "Виберіть симптоми, що вас турбують та отримайте ймовірний діагноз"))

        self.label_17.setText(_translate("MainWindow", "Ім\'я"))
        self.label_18.setText(_translate("MainWindow", "Прізвище"))


        self.label_23.setText(_translate("MainWindow", "Останній діагноз"))
        self.label_24.setText(_translate("MainWindow", "Інформація про користувача"))
        self.Name_1.setText(_translate("MainWindow", "Алла Клочко"))
        self.Education_1.setText(_translate("MainWindow", "Освіта: Львівський національний університет імені Івана Франка"))
        self.Doctor_1_Category_1.setText(_translate("MainWindow", "Серцево-судинні захворювання"))
        self.Doctor_1_Category_2.setText(_translate("MainWindow", "Статева система"))
        self.Doctor_1_Category_3.setText(_translate("MainWindow", "Інфекції"))
        self.Doctor_1_Experience.setText(_translate("MainWindow", "Досвід: 10 років"))
        self.Doctor_1_Description.setText(_translate("MainWindow", "Алла Іванівна Клочко більше 10-ти років займається оглядами, вигодовуванням дітей раннього віку, діагностикою та лікуванням захворювань у дітей з позицій доказової медицини. Лікар щорічно відвідує курси тематичного вдосконалення, належить до Асоціації педіатрів і нутріціологів України."))
        self.contact_button_1.setText(_translate("MainWindow", "Зв’язатись з лікарем"))
        self.search_line_2.setPlaceholderText(_translate("MainWindow", "Пошук лікаря"))
        self.symptoms_list_2.setToolTip(_translate("MainWindow", "Кашель"))
        self.symptoms_list_2.setSortingEnabled(False)
        self.recommended_button.setText(_translate("MainWindow", "Дізнатись більше"))
        self.label_12.setText(_translate("MainWindow", "Пошук за спеціальністю"))
        self.Doctor_2_Name.setText(_translate("MainWindow", "Олександра Кравчук"))
        self.Doctor_2_Education.setText(_translate("MainWindow", "Освіта: Львівський національний університет імені Івана Франка"))
        self.Doctor_2_Category_1.setText(_translate("MainWindow", "Нервова система"))
        self.Doctor_2_Category_2.setText(_translate("MainWindow", "Травми"))
        self.Doctor_2_Category_3.setText(_translate("MainWindow", "Хвороба очей"))
        self.Doctor_2_Experience.setText(_translate("MainWindow", "Досвід: 6 років"))
        self.Doctor_2_Description.setText(_translate("MainWindow", "Олександра Іванівна Кравчук більше 6-ти років займається оглядами, вигодовуванням дітей раннього віку, діагностикою та лікуванням захворювань у дітей з позицій доказової медицини. Лікар щорічно відвідує курси тематичного вдосконалення, належить до Асоціації педіатрів і нутріціологів України."))
        self.contact_button_2.setText(_translate("MainWindow", "Зв’язатись з лікарем"))
import resources_2




if __name__ == "__main__":


    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Menu()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

