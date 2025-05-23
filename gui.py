from PyQt6.QtWidgets import *
from mainwindow import Ui_MainWindow
from exam import Exam
from course import Course
from result import Result

# test Course
klasse = Course("klasse", "sek1", ["Schüler1", "Schüler2", "Schüler3"])

# test Exam
lk = Exam("lk", "")
lk.add_task("A1", 5)
lk.add_task("A2", 4)

courselist = [klasse]
examlist = [lk]


def search_exam(name: str, list: list):
    """
        Durchsucht eine liste von Klausuren anhand eines Namen

        Args:
            name (str): Name der gesuchten Klausur
            list (list): Zu durchsuchende Liste
        Returns:
            Exam: gesuchte Klausur
    """

    for i in list:
        if i.exam_name == name:
            return (i)


def search_course(name: str, list: list):
    """
        Durchsucht eine liste von Kursen anhand eines Namen

        Args:
            name (str): Name des gesuchten Kurses
            list (list): Zu durchsuchende Liste
        Returns:
            Course: gesuchter Kurs
    """

    for i in list:
        if i.course_name == name:
            return (i)


def confirm_input():
    """
        Startet show_evaluation_table
    """
    course = search_course(ui.choose_course_textEdit.toPlainText(), courselist)
    exam = search_exam(ui.choose_exam_textEdit.toPlainText(), examlist)

    show_evaluation_table(course, exam)


def show_evaluation_table(course: Course, exam: Exam):
    """
        Erstellt die Tabelle zur Eingabe der Bewertung

        Args:
            course (Course): ausgewählter Kurs
            exam (Exam): ausgewählte Klausur/Test/LK
    """

    # Spalten und Zeilen festlegen
    ui.evaluation_input_tableWidget.setRowCount(len(course.student_names) + 2)
    ui.evaluation_input_tableWidget.setColumnCount(len(exam.tasks) + 2)

    # Beschriftungen Einfügen
    ui.evaluation_input_tableWidget.setItem(0, 0, QTableWidgetItem("Aufgabe:"))
    ui.evaluation_input_tableWidget.setItem(1, 0, QTableWidgetItem("Max BE"))
    ui.evaluation_input_tableWidget.setItem(0, len(exam.tasks) + 1, QTableWidgetItem("Gesamt"))
    ui.evaluation_input_tableWidget.setItem(1, len(exam.tasks) + 1, QTableWidgetItem(str(exam.max_points)))

    #  Schülernamen Einfügen
    for i in range(len(course.student_names)):
        ui.evaluation_input_tableWidget.setItem(2 + i, 0, QTableWidgetItem(course.student_names[i]))

    # Aufgabennamen mit BE Einfügen
    for i in range(len(exam.tasks)):
        task_name = list(exam.tasks.keys())[i]
        task_points = exam.tasks[task_name]
        ui.evaluation_input_tableWidget.setItem(0, i + 1, QTableWidgetItem(task_name))
        ui.evaluation_input_tableWidget.setItem(1, i + 1, QTableWidgetItem(str(task_points)))


def confirm_evaluation():
    """
        Erstellt ein Objekt der Klasse Result aus den Eingaben
        """

    # Eingegebene Daten lesen
    course = search_course(ui.choose_course_textEdit.toPlainText(), courselist)
    exam = search_exam(ui.choose_exam_textEdit.toPlainText(), examlist)
    date = ui.date_textEdit.toPlainText()

    result = Result([course], [], date, exam)

    for i in range(len(course.student_names)):
        # Daten des Schülers definieren
        student_name = course.student_names[i]
        points_earned = 0
        tasks = {}

        for j in range(len(exam.tasks)):
            # Dictionary der Aufgaben mit Erreichten Punkten eines Schülers definieren
            task_name = list(exam.tasks.keys())[j]
            scored_points_task = int(ui.evaluation_input_tableWidget.item(i + 2, j + 1).text())
            tasks[task_name] = scored_points_task

            points_earned = points_earned + scored_points_task

        percentage_earned = (points_earned / exam.max_points) * 100

        # Eintrag im Ergebnis für den Schüler
        result.add_result(student_name, points_earned, percentage_earned, tasks)


app = QApplication([])
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

# Verknüpfung der Buttons mit Funktionen
ui.confirm_input_pushButton.clicked.connect(confirm_input)
ui.confirm_evaluation_pushButton.clicked.connect(confirm_evaluation)

window.show()

app.exec()
