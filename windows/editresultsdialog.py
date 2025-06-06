# Form implementation generated from reading ui file 'windows/editresultsdialog.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_edit_result_dialog(object):
    def setupUi(self, edit_result_dialog):
        edit_result_dialog.setObjectName("edit_result_dialog")
        edit_result_dialog.resize(492, 459)
        edit_result_dialog.setStyleSheet("background-color: rgb(206, 211, 196);")
        self.label = QtWidgets.QLabel(parent=edit_result_dialog)
        self.label.setGeometry(QtCore.QRect(0, 10, 491, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.select_exam_box = QtWidgets.QComboBox(parent=edit_result_dialog)
        self.select_exam_box.setGeometry(QtCore.QRect(10, 40, 471, 22))
        self.select_exam_box.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-radius:  10px;\n"
"font: 14px;\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(151, 145, 174);")
        self.select_exam_box.setObjectName("select_exam_box")
        self.select_course_box = QtWidgets.QComboBox(parent=edit_result_dialog)
        self.select_course_box.setGeometry(QtCore.QRect(10, 70, 471, 22))
        self.select_course_box.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-radius:  10px;\n"
"font: 14px;\n"
"color: rgb(0, 0, 0);\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(151, 145, 174);")
        self.select_course_box.setObjectName("select_course_box")
        self.date_edit = QtWidgets.QLineEdit(parent=edit_result_dialog)
        self.date_edit.setGeometry(QtCore.QRect(10, 100, 471, 21))
        self.date_edit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-radius:  10px;\n"
"font: 14px;\n"
"color: rgb(0, 0, 0);")
        self.date_edit.setObjectName("date_edit")
        self.generate_table_button = QtWidgets.QPushButton(parent=edit_result_dialog)
        self.generate_table_button.setGeometry(QtCore.QRect(10, 130, 471, 24))
        self.generate_table_button.setStyleSheet("background-color: rgb(216, 204, 231);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius:  10px;\n"
"border-color: black;\n"
"border-color: gray;\n"
"font: 14px;")
        self.generate_table_button.setObjectName("generate_table_button")
        self.results_table = QtWidgets.QTableWidget(parent=edit_result_dialog)
        self.results_table.setGeometry(QtCore.QRect(10, 160, 471, 231))
        self.results_table.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-radius:  10px;\n"
"font: 14px;\n"
"")
        self.results_table.setObjectName("results_table")
        self.results_table.setColumnCount(0)
        self.results_table.setRowCount(0)
        self.save_button = QtWidgets.QPushButton(parent=edit_result_dialog)
        self.save_button.setGeometry(QtCore.QRect(10, 400, 231, 24))
        self.save_button.setStyleSheet("background-color: rgb(127, 169, 112);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius:  10px;\n"
"border-color: white;\n"
"font: bold 14px;")
        self.save_button.setObjectName("save_button")
        self.exit_button = QtWidgets.QPushButton(parent=edit_result_dialog)
        self.exit_button.setGeometry(QtCore.QRect(250, 400, 231, 24))
        self.exit_button.setStyleSheet("background-color: rgb(127, 169, 112);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius:  10px;\n"
"border-color: white;\n"
"font: bold 14px;")
        self.exit_button.setObjectName("exit_button")
        self.print_button = QtWidgets.QPushButton(parent=edit_result_dialog)
        self.print_button.setGeometry(QtCore.QRect(10, 430, 231, 24))
        self.print_button.setStyleSheet("background-color: rgb(127, 169, 112);\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius:  10px;\n"
"border-color: white;\n"
"font: bold 14px;")
        self.print_button.setObjectName("print_button")

        self.retranslateUi(edit_result_dialog)
        self.exit_button.clicked.connect(edit_result_dialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(edit_result_dialog)

    def retranslateUi(self, edit_result_dialog):
        _translate = QtCore.QCoreApplication.translate
        edit_result_dialog.setWindowTitle(_translate("edit_result_dialog", "Ergebnisse bearbeiten/hinzufügen"))
        self.label.setText(_translate("edit_result_dialog", "Ergebnisse bearbeiten/hinzufügen"))
        self.date_edit.setPlaceholderText(_translate("edit_result_dialog", "Datum"))
        self.generate_table_button.setText(_translate("edit_result_dialog", "Tabelle generieren"))
        self.save_button.setText(_translate("edit_result_dialog", "Speichern"))
        self.exit_button.setText(_translate("edit_result_dialog", "Abbrechen"))
        self.print_button.setText(_translate("edit_result_dialog", "Drucken"))
