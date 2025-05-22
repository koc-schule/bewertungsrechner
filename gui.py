from PyQt6.QtWidgets import *
from mainwindow import Ui_MainWindow
from test import Exam
from test import Course

# tests
klasse = Course("klasse", ["Schüler1", "Schüler2", "Schüler3"])
lk = Exam("lk", ["eins", "zwei", "drei"])

courselist = [klasse]
examlist = [lk]


def search_exam(name, list):
    for i in list:
        if i.exam_name == name:
            print("jaa")
            return (i)


def search_course(name, list):
    for i in list:
        if i.course_name == name:
            return (i)


def confirm_input():
    date = ui.date_textEdit.toPlainText()

    course = search_course(ui.choose_course_textEdit.toPlainText(), courselist)
    exam = search_exam(ui.choose_exam_textEdit.toPlainText(), examlist)

    show_evaluation_table(course, exam)

def show_evaluation_table(course, exam):
    # Spalten und Zeilen festlegen
    ui.evaluation_input_tableWidget.setRowCount(len(course.student_names) + 2)
    ui.evaluation_input_tableWidget.setColumnCount(len(exam.tasks) + 2)

    # Vorgegebene Items festlegen
    ui.evaluation_input_tableWidget.setItem(0, 0, QTableWidgetItem("Aufgabe:"))
    ui.evaluation_input_tableWidget.setItem(1, 0, QTableWidgetItem("Max BE"))
    ui.evaluation_input_tableWidget.setItem(0, len(course.student_names) + 1, QTableWidgetItem("Gesamt"))

    #  Schülernamen Einfügen
    for i in range(len(course.student_names)):
        ui.evaluation_input_tableWidget.setItem(2 + i, 0, QTableWidgetItem(course.student_names[i]))


app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

ui.confirm_input_pushButton.clicked.connect(confirm_input)
# ui.confirm_evaluation_pushButton.clicked.connect()

window.show()

app.exec()
