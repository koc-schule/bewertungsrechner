from PyQt6.QtWidgets import *
from windows.mainwindow import Ui_MainWindow
from windows.editcoursedialog import Ui_edit_course_dialog
from windows.viewcoursedialog import Ui_view_course_dialog
from windows.viewexamdialog import Ui_view_exam_dialog
from windows.editexamdialog import Ui_edit_exam_dialog
from windows.viewresultdialog import Ui_view_result_dialog
from windows.editresultsdialog import Ui_edit_result_dialog
from exam import Exam
from course import Course
from result import Result
from utils.json_parser import *
from utils.parser import csv_to_result
import os

# test Course
klasse = Course("klasse", "sek1", ["Schüler1", "Schüler2", "Schüler3"])

# test Exam
lk = Exam("lk", "")
lk.add_task("A1", 5)
lk.add_task("A2", 4)

course_list = []
exam_list = []
result_list = []

selected_course = None
selected_exam = None
selected_date = ""

def get_exams():
    names = [
    f.removeprefix("exam_").removesuffix(".json")
    for f in os.listdir("exams/")
    if f.startswith("exam_") and f.endswith(".json")
    ]
    return names

def get_courses():
    names = [
    f.removeprefix("course_").removesuffix(".json")
    for f in os.listdir("courses/")
    if f.startswith("course_") and f.endswith(".json")
    ]
    return names

def get_results():
    results = [
    f.removesuffix(".csv")
    for f in os.listdir("results/")
    if f.endswith(".csv")
    ]
    return results


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

def show_evaluation_table():
    """
        Erstellt die Tabelle zur Eingabe der Bewertung

        Args:
            course (Course): ausgewählter Kurs
            exam (Exam): ausgewählte Klausur/Test/LK
    """
    global selected_course
    global selected_exam
    global selected_date

    selected_course = json_to_course(mainwindow_ui.select_course_box.currentText())
    selected_exam = json_to_exam(mainwindow_ui.select_exam_box.currentText())
    selected_date = mainwindow_ui.date_edit.text()

    # Spalten und Zeilen festlegen
    mainwindow_ui.evaluation_input_tableWidget.setRowCount(len(selected_course.student_names) + 2)
    mainwindow_ui.evaluation_input_tableWidget.setColumnCount(len(selected_exam.tasks) + 2)

    # Beschriftungen Einfügen
    mainwindow_ui.evaluation_input_tableWidget.setItem(0, 0, QTableWidgetItem("Aufgabe:"))
    mainwindow_ui.evaluation_input_tableWidget.setItem(1, 0, QTableWidgetItem("Max BE"))
    mainwindow_ui.evaluation_input_tableWidget.setItem(0, len(selected_exam.tasks) + 1, QTableWidgetItem("Gesamt"))
    mainwindow_ui.evaluation_input_tableWidget.setItem(1, len(selected_exam.tasks) + 1, QTableWidgetItem(str(selected_exam.max_points)))

    #  Schülernamen Einfügen
    for i in range(len(selected_course.student_names)):
        mainwindow_ui.evaluation_input_tableWidget.setItem(2 + i, 0, QTableWidgetItem(selected_course.student_names[i]))

    # Aufgabennamen mit BE Einfügen
    for i in range(len(selected_exam.tasks)):
        task_name = list(selected_exam.tasks.keys())[i]
        task_points = selected_exam.tasks[task_name]
        mainwindow_ui.evaluation_input_tableWidget.setItem(0, i + 1, QTableWidgetItem(task_name))
        mainwindow_ui.evaluation_input_tableWidget.setItem(1, i + 1, QTableWidgetItem(str(task_points)))


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
            scored_points_task = int(mainwindow_ui.evaluation_input_tableWidget.item(i + 2, j + 1).text())
            tasks[task_name] = scored_points_task

            points_earned = points_earned + scored_points_task

        percentage_earned = (points_earned / selected_exam.max_points) * 100

        # Eintrag im Ergebnis für den Schüler
        result.add_result(student_name, points_earned, percentage_earned, tasks)
    
    result.write_to_csv()

def show_edit_course_window() -> None:
    """
    Ziegt das Fenster zum Hinzufügen eines Kurses an
    """
    # Leeren aller Felder für cleaneren Look
    edit_course_ui.name_input.clear()
    edit_course_ui.sek_input.setCurrentIndex(0)
    edit_course_ui.add_student_input.clear()
    edit_course_ui.students_textbox.clear()

    edit_course_window.show()

def add_student_to_list() -> None:
    """
    Fügt den Namen in add_student_input zur students_textbox hinzu
    """
    name = edit_course_ui.add_student_input.text()
    edit_course_ui.students_textbox.appendPlainText(name)
    edit_course_ui.add_student_input.clear() # Leeren des Inputs für cleanere zweite Eingabe

def save_course() -> None:
    """
    Liest die Daten aus der UI, erstellt und speichert einen neuen Kurs
    """
    # Auslesen der Daten
    name = edit_course_ui.name_input.text()
    grading_scheme = ""
    if edit_course_ui.sek_input.currentIndex() == 0:
        grading_scheme = "sek1"
    if edit_course_ui.sek_input.currentIndex() == 1:
        grading_scheme = "sek2"
    students_raw = edit_course_ui.students_textbox.toPlainText()
    students = students_raw.strip().split('\n')
    # Erstellen und Speichern des neuen Kurses
    new_course = Course(name, grading_scheme, students)
    course_to_json(new_course)
    update_content()
    edit_course_window.close()

def show_view_course_window() -> None:
    """
    Zeigt das Fenster zur Auswahl von Kursen an
    """
    view_course_ui.select_course_box.clear()
    view_course_ui.select_course_box.addItems(course_list)
    view_course_window.show()

def view_course() -> None:
    """
    Öffnen eines Kurses im Kurs-Bearbeitungs-Fenster aus einer JSON Datei
    """
    # Erstellen des neuen Kurs objects aus JSON
    course_name = view_course_ui.select_course_box.currentText()
    course = json_to_course(course_name)
    # Einfügen der Kurs-Daten in die UI
    edit_course_ui.name_input.setText(course.course_name)
    edit_course_ui.add_student_input.clear()
    edit_course_ui.students_textbox.clear()
    if course.grading_scheme == 'sek1':
        edit_course_ui.sek_input.setCurrentIndex(0)
    if course.grading_scheme == 'sek2':
        edit_course_ui.sek_input.setCurrentIndex(1)
    for student in course.student_names:
        edit_course_ui.students_textbox.appendPlainText(student)
    
    edit_course_window.show()
    view_course_window.close()

def show_view_exam_window() -> None:
    """
    Ziegt das Fenster zur Auswahl von Klausuren an
    """
    view_exam_ui.select_exam_box.clear()
    view_exam_ui.select_exam_box.addItems(exam_list)
    view_exam_window.show()

def view_exam() -> None:
    """
    Öffnen einer Klausur im Klausur-Bearbeitungs-Fenster aus einer JSON Datei
    """
    exam_name = view_exam_ui.select_exam_box.currentText()
    exam = json_to_exam(exam_name)
    edit_exam_ui.name_input.setText(exam.exam_name)
    edit_exam_ui.notes_textbox.setPlainText(exam.notes)
    edit_exam_ui.add_task_input.clear()
    edit_exam_ui.tasks_textbox.clear()
    for task_name, points in exam.tasks.items():
        output = f"{task_name}:{points}"
        edit_exam_ui.tasks_textbox.appendPlainText(output)
    
    edit_exam_window.show()
    view_exam_window.close()

def show_edit_exam_window() -> None:
    """
    Zeigt das Fenster zum Hinzufügen einer Klausur an
    """
    # Leeren der Felder für einen cleaneren Look
    edit_exam_ui.name_input.clear()
    edit_exam_ui.notes_textbox.clear()
    edit_exam_ui.add_task_input.clear()
    edit_exam_ui.tasks_textbox.clear()

    edit_exam_window.show()

def add_task_to_list() -> None:
    task = edit_exam_ui.add_task_input.text()
    edit_exam_ui.tasks_textbox.appendPlainText(task)
    edit_exam_ui.add_task_input.clear()

def save_exam() -> None:
    """
    Liest die Daten aus der UI, erstellt und speichert eine neue Klausur
    """
    name = edit_exam_ui.name_input.text()
    notes = edit_exam_ui.notes_textbox.toPlainText()
    tasks = edit_exam_ui.tasks_textbox.toPlainText()
    new_exam = Exam(name, notes)
    for line in tasks.strip().splitlines():
        if ":" in line:
            task_name, points = line.split(":", 1)
            new_exam.add_task(task_name, int(points))
    exam_to_json(new_exam)
    update_content()
    edit_exam_window.close()

def show_view_result_window() -> None:
    view_result_ui.select_result_box.clear
    view_result_ui.select_result_box.addItems(result_list)
    view_result_window.show()

def show_edit_result_window() -> None:
    edit_result_ui.select_course_box.clear()
    edit_result_ui.select_course_box.addItems(course_list)
    edit_result_ui.select_exam_box.clear()
    edit_result_ui.select_exam_box.addItems(exam_list)
    edit_result_ui.date_edit.clear()
    edit_result_ui.results_table.clear()

    edit_result_window.show()

def load_results_table() -> None:
    """
        Erstellt die Tabelle zur Eingabe der Bewertung

        Args:
            course (Course): ausgewählter Kurs
            exam (Exam): ausgewählte Klausur/Test/LK
    """
    global selected_course
    global selected_exam
    global selected_date

    selected_course = json_to_course(edit_result_ui.select_course_box.currentText())
    selected_exam = json_to_exam(edit_result_ui.select_exam_box.currentText())
    selected_date = edit_result_ui.date_edit.text()

    # Spalten und Zeilen festlegen
    edit_result_ui.results_table.setRowCount(len(selected_course.student_names) + 2)
    edit_result_ui.results_table.setColumnCount(len(selected_exam.tasks) + 2)

    # Beschriftungen Einfügen
    edit_result_ui.results_table.setItem(0, 0, QTableWidgetItem("Aufgabe:"))
    edit_result_ui.results_table.setItem(1, 0, QTableWidgetItem("Max BE"))
    edit_result_ui.results_table.setItem(0, len(selected_exam.tasks) + 1, QTableWidgetItem("Gesamt"))
    edit_result_ui.results_table.setItem(1, len(selected_exam.tasks) + 1, QTableWidgetItem(str(selected_exam.max_points)))

    #  Schülernamen Einfügen
    for i in range(len(selected_course.student_names)):
        edit_result_ui.results_table.setItem(2 + i, 0, QTableWidgetItem(selected_course.student_names[i]))

    # Aufgabennamen mit BE Einfügen
    for i in range(len(selected_exam.tasks)):
        task_name = list(selected_exam.tasks.keys())[i]
        task_points = selected_exam.tasks[task_name]
        edit_result_ui.results_table.setItem(0, i + 1, QTableWidgetItem(task_name))
        edit_result_ui.results_table.setItem(1, i + 1, QTableWidgetItem(str(task_points)))

def save_results() -> None:
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
            scored_points_task = int(edit_result_ui.results_table.item(i + 2, j + 1).text())
            tasks[task_name] = scored_points_task

            points_earned = points_earned + scored_points_task

        percentage_earned = (points_earned / selected_exam.max_points) * 100

        # Eintrag im Ergebnis für den Schüler
        result.add_result(student_name, points_earned, percentage_earned, tasks)
    
    result.write_to_csv()
    update_content()
    edit_result_window.close()

def fill_results_table(result) -> None:
    """
    Füllt die Ergebnisse aus einem Result-Objekt in das TableWidget im Result-Editor.
    """
    # Setze Kurs und Klausur für die aktuelle Ansicht
    course = result.courses[0]
    exam = result.exam

    # Optional: Tabelle vorbereiten (Größe und Header)
    edit_result_ui.results_table.setRowCount(len(course.student_names) + 2)
    edit_result_ui.results_table.setColumnCount(len(exam.tasks) + 2)

    # Header wie in load_results_table setzen
    edit_result_ui.results_table.setItem(0, 0, QTableWidgetItem("Aufgabe:"))
    edit_result_ui.results_table.setItem(1, 0, QTableWidgetItem("Max BE"))
    edit_result_ui.results_table.setItem(0, len(exam.tasks) + 1, QTableWidgetItem("Gesamt"))
    edit_result_ui.results_table.setItem(1, len(exam.tasks) + 1, QTableWidgetItem(str(exam.max_points)))

    # Schülernamen eintragen
    for i, student_name in enumerate(course.student_names):
        edit_result_ui.results_table.setItem(2 + i, 0, QTableWidgetItem(student_name))

    # Aufgaben eintragen
    for j, (task_name, task_points) in enumerate(exam.tasks.items()):
        edit_result_ui.results_table.setItem(0, j + 1, QTableWidgetItem(task_name))
        edit_result_ui.results_table.setItem(1, j + 1, QTableWidgetItem(str(task_points)))

    # Ergebnisse eintragen
    for i, student_name in enumerate(course.student_names):
        # Finde das Ergebnis für den Schüler
        student_result = next((r for r in result.results if r["name"] == student_name), None)
        if student_result:
            total_points = student_result.get("points_earned", 0)
            edit_result_ui.results_table.setItem(2 + i, len(exam.tasks) + 1, QTableWidgetItem(str(total_points)))
            for j, task_name in enumerate(exam.tasks.keys()):
                points = student_result.get(task_name, 0)
                edit_result_ui.results_table.setItem(2 + i, j + 1, QTableWidgetItem(str(points)))

def view_result() -> None:
    result_name = view_result_ui.select_result_box.currentText()
    result = csv_to_result(result_name)

    edit_result_ui.select_exam_box.clear()
    edit_result_ui.select_exam_box.addItems(exam_list)
    edit_result_ui.select_course_box.clear()
    edit_result_ui.select_course_box.addItems(course_list)
    edit_result_ui.select_exam_box.setCurrentText(result.exam.exam_name)
    edit_result_ui.select_course_box.setCurrentText(result.courses[0].course_name)
    edit_result_ui.date_edit.setText(result.date)
    load_results_table()
    fill_results_table(result)

    edit_result_window.show()
    view_result_window.close()

def update_content() -> None:
    """
    Update Funktion für z.B. die globale Kurs- und Klausurliste
    """
    global exam_list
    global course_list
    global result_list
    exam_list = get_exams()
    course_list = get_courses()
    result_list = get_results()
    mainwindow_ui.select_course_box.clear()
    mainwindow_ui.select_course_box.addItems(course_list)
    mainwindow_ui.select_exam_box.clear()
    mainwindow_ui.select_exam_box.addItems(exam_list)

app = QApplication([])
mainwindow = QMainWindow()
mainwindow_ui = Ui_MainWindow()
mainwindow_ui.setupUi(mainwindow)
edit_course_window = QDialog()
edit_course_ui = Ui_edit_course_dialog()
edit_course_ui.setupUi(edit_course_window)
view_course_window = QDialog()
view_course_ui = Ui_view_course_dialog()
view_course_ui.setupUi(view_course_window)
view_exam_window = QDialog()
view_exam_ui = Ui_view_exam_dialog()
view_exam_ui.setupUi(view_exam_window)
edit_exam_window = QDialog()
edit_exam_ui = Ui_edit_exam_dialog()
edit_exam_ui.setupUi(edit_exam_window)
view_result_window = QDialog()
view_result_ui = Ui_view_result_dialog()
view_result_ui.setupUi(view_result_window)
edit_result_window = QDialog()
edit_result_ui = Ui_edit_result_dialog()
edit_result_ui.setupUi(edit_result_window)

# Verknüpfung der Buttons mit Funktionen
mainwindow_ui.confirm_input_pushButton.clicked.connect(show_evaluation_table)
mainwindow_ui.confirm_evaluation_pushButton.clicked.connect(confirm_evaluation)
mainwindow_ui.actionCourseAdd.triggered.connect(show_edit_course_window)
mainwindow_ui.actionCourseView.triggered.connect(show_view_course_window)
mainwindow_ui.actionExamAdd.triggered.connect(show_edit_exam_window)
mainwindow_ui.actionExamView.triggered.connect(show_view_exam_window)
mainwindow_ui.actionResultView.triggered.connect(show_view_result_window)
mainwindow_ui.actionResultAdd.triggered.connect(show_edit_result_window)

edit_course_ui.save_button.clicked.connect(save_course)
edit_course_ui.add_student_button.clicked.connect(add_student_to_list)

edit_exam_ui.add_task_button.clicked.connect(add_task_to_list)
edit_exam_ui.save_button.clicked.connect(save_exam)

view_course_ui.view_button.clicked.connect(view_course)
view_exam_ui.view_button.clicked.connect(view_exam)
view_result_ui.view_button.clicked.connect(view_result)

edit_result_ui.generate_table_button.clicked.connect(load_results_table)
edit_result_ui.save_button.clicked.connect(save_results)

update_content()

mainwindow.show()

app.exec()
