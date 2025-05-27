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

course_list = [klasse]
exam_list = [lk]

selected_course = None
selected_exam = None
selected_date = ""


def search_exam(searched_exam: str, exam_list: list):
    """
        Durchsucht die Liste von Klausuren nach einer spezifischen Klausur nach Name

        Args:
            searched_exam (str): Name der gesuchten Klausur
            exam_list (list): Zu durchsuchende Liste
        Returns:
            exam (Exam): gesuchte Klausur
    """

    for exam in exam_list:
        if exam.exam_name == searched_exam:
            return (exam)


def search_course(searched_course: str, course_list: list):
    """
        Durchsucht eine liste von Kursen anhand eines Namen

        Args:
            searched_course (str): Name des gesuchten Kurses
            course_list (list): Zu durchsuchende Liste
        Returns:
            course (Course): gesuchter Kurs
    """

    for course in course_list:
        if course.course_name == searched_course:
            return (course)


def confirm_input():
    global selected_course
    global selected_exam
    global selected_date
    """
        Startet show_evaluation_table
    """
    selected_course = search_course(ui.choose_course_textEdit.toPlainText(), course_list)
    selected_exam = search_exam(ui.choose_exam_textEdit.toPlainText(), exam_list)
    selected_date = ui.date_textEdit.toPlainText()

    # Checks if Exam and Course were properly selected
    if (selected_course is not None) and (selected_exam is not None):
        show_evaluation_table(selected_course, selected_exam)
    elif selected_course is None:
        print("Course not in Courselist")
        ui.choose_course_textEdit.clear()
    elif selected_exam is None:
        print("Exam not in Examlist")
        ui.choose_exam_textEdit.clear()


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

    result = Result([selected_course], [], selected_date, selected_exam)

    for i in range(len(selected_course.student_names)):
        # Daten des Schülers definieren
        student_name = selected_course.student_names[i]
        points_earned = 0
        tasks = {}

        for j in range(len(selected_exam.tasks)):
            # Dictionary der Aufgaben mit Erreichten Punkten eines Schülers definieren
            task_name = list(selected_exam.tasks.keys())[j]
            scored_points_task = int(ui.evaluation_input_tableWidget.item(i + 2, j + 1).text())
            tasks[task_name] = scored_points_task

            points_earned = points_earned + scored_points_task

        percentage_earned = (points_earned / selected_exam.max_points) * 100

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
