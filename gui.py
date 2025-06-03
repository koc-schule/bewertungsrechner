from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from printer import printer_templates
from windows.mainwindow import Ui_MainWindow
from windows.editcoursedialog import Ui_edit_course_dialog
from windows.editexamdialog import Ui_edit_exam_dialog
from windows.editresultsdialog import Ui_edit_result_dialog
from windows.deletedialog import Ui_delete_dialog
from windows.viewdialog import Ui_view_dialog
from windows.printdialog import Ui_print_dialog
from exam import Exam
from course import Course
from result import Result
from utils.json_parser import *
from utils.parser import csv_to_result
import os
from printer import log

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
    if not os.path.isdir("exams/"):
        os.mkdir("exams/")
    names = [
    f.removeprefix("exam_").removesuffix(".json")
    for f in os.listdir("exams/")
    if f.startswith("exam_") and f.endswith(".json")
    ]
    return names

def get_courses():
    if not os.path.isdir("courses/"):
        os.mkdir("courses/")
    names = [
    f.removeprefix("course_").removesuffix(".json")
    for f in os.listdir("courses/")
    if f.startswith("course_") and f.endswith(".json")
    ]
    return names

def get_results():
    if not os.path.isdir("results/"):
        os.mkdir("results/")
    results = [
    f.removesuffix(".csv")
    for f in os.listdir("results/")
    if f.endswith(".csv")
    ]
    return results 

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
    if name is not "":
        new_course = Course(name, grading_scheme, students)
        course_to_json(new_course)
        update_content()
        edit_course_window.close()
    else:
        edit_course_ui.name_input.setText("Bitte einen Namen eingeben!")

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

def show_delete_course_window():
    delete_window.setWindowTitle("Kurs löschen")
    delete_ui.select_box.clear()
    delete_ui.select_box.addItems(course_list)
    delete_ui.delete_button.disconnect()
    delete_ui.delete_button.clicked.connect(delete_course)
    delete_window.show()

def delete_course():
    name = delete_ui.select_box.currentText()
    os.remove(f"courses/course_{name}.json")
    update_content()
    delete_window.close()

def show_delete_exam_window():
    delete_window.setWindowTitle("Klausur löschen")
    delete_ui.select_box.clear()
    delete_ui.select_box.addItems(exam_list)
    delete_ui.delete_button.disconnect()
    delete_ui.delete_button.clicked.connect(delete_exam)
    delete_window.show()

def delete_exam():
    name = delete_ui.select_box.currentText()
    os.remove(f"exams/exam_{name}.json")
    update_content()
    delete_window.close()

def show_delete_result_window():
    delete_window.setWindowTitle("Ergebnisse löschen")
    delete_ui.select_box.clear()
    delete_ui.select_box.addItems(result_list)
    delete_ui.delete_button.disconnect()
    delete_ui.delete_button.clicked.connect(delete_result)
    delete_window.show()

def delete_result():
    name = delete_ui.select_box.currentText()
    os.remove(f"results/{name}.csv")
    update_content()
    delete_window.close()

def show_view_course_window() -> None:
    """
    Zeigt das Fenster zur Auswahl von Kursen an
    """
    view_window.setWindowTitle("Kurs bearbeiten")
    view_ui.select_box.clear()
    view_ui.select_box.addItems(course_list)
    view_ui.view_button.disconnect()
    view_ui.view_button.clicked.connect(view_course)
    view_window.show()

def view_course() -> None:
    """
    Öffnen eines Kurses im Kurs-Bearbeitungs-Fenster aus einer JSON Datei
    """
    # Erstellen des neuen Kurs objects aus JSON
    course_name = view_ui.select_box.currentText()
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
    view_window.close()

def show_view_exam_window() -> None:
    """
    Zeigt das Fenster zur Auswahl von Kursen an
    """
    view_window.setWindowTitle("Klausur bearbeiten")
    view_ui.select_box.clear()
    view_ui.select_box.addItems(exam_list)
    view_ui.view_button.disconnect()
    view_ui.view_button.clicked.connect(view_exam)
    view_window.show()

def view_exam() -> None:
    """
    Öffnen einer Klausur im Klausur-Bearbeitungs-Fenster aus einer JSON Datei
    """
    exam_name = view_ui.select_box.currentText()
    exam = json_to_exam(exam_name)
    edit_exam_ui.name_input.setText(exam.exam_name)
    edit_exam_ui.notes_textbox.setPlainText(exam.notes)
    edit_exam_ui.add_task_input.clear()
    edit_exam_ui.tasks_textbox.clear()
    for task_name, points in exam.tasks.items():
        output = f"{task_name}:{points}"
        edit_exam_ui.tasks_textbox.appendPlainText(output)
    
    edit_exam_window.show()
    view_window.close()

def show_view_result_window() -> None:
    """
    Zeigt das Fenster zur Auswahl von Ergebnissen an
    """
    view_window.setWindowTitle("Ergebnisse bearbeiten")
    view_ui.select_box.clear()
    view_ui.select_box.addItems(result_list)
    view_ui.view_button.disconnect()
    view_ui.view_button.clicked.connect(view_result)
    view_window.show()

def view_result() -> None:
    result_name = view_ui.select_box.currentText()
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
    view_window.close()

def show_print_window() -> None:
    print_ui.student_list.clear()
    course_name = edit_result_ui.select_course_box.currentText()
    exam_name = edit_result_ui.select_exam_box.currentText()
    result_name = f"{course_name}_{exam_name}"
    result = csv_to_result(result_name)
    print_ui.resultname_label.setText(result_name)

    for student in result.courses[0].student_names:
        item = QListWidgetItem(student)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        print_ui.student_list.addItem(item)
    
    print_window.show()

def select_all_students() -> None:
    for i in range(print_ui.student_list.count()):
        item = print_ui.student_list.item(i)
        item.setCheckState(Qt.CheckState.Checked)

def print_students():
    log.log("1.")
    student_names = []
    for i in range(print_ui.student_list.count()):
        log.log(f"{i} clause")
        item = print_ui.student_list.item(i)
        if item.checkState() == Qt.CheckState.Checked:
            student_names.append(item.text())
    
    log.log("2.")

    result = csv_to_result(print_ui.resultname_label.text())
    log.log("3.")
    list_infos = result.gather_print_information(student_names)
    log.log("4.")
    for i in list_infos:
        printer_templates.PrinterTemplates.student_result_receipt(**i)

def print_analysis():
    try:
        log.log("1.")
        result = csv_to_result(print_ui.resultname_label.text())
        log.log("2.")
        infos = result.result_analysis()
        log.log("3.")
        printer_templates.PrinterTemplates.course_result_receipt(**infos)
        log.log("4.")
    except Exception as e:
        log.log(str(e))

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

app = QApplication([])
mainwindow = QMainWindow()
mainwindow_ui = Ui_MainWindow()
mainwindow_ui.setupUi(mainwindow)
edit_course_window = QDialog()
edit_course_ui = Ui_edit_course_dialog()
edit_course_ui.setupUi(edit_course_window)
edit_exam_window = QDialog()
edit_exam_ui = Ui_edit_exam_dialog()
edit_exam_ui.setupUi(edit_exam_window)
edit_result_window = QDialog()
edit_result_ui = Ui_edit_result_dialog()
edit_result_ui.setupUi(edit_result_window)
delete_window = QDialog()
delete_ui = Ui_delete_dialog()
delete_ui.setupUi(delete_window)
view_window = QDialog()
view_ui = Ui_view_dialog()
view_ui.setupUi(view_window)
print_window = QDialog()
print_ui = Ui_print_dialog()
print_ui.setupUi(print_window)

# Verknüpfung der Buttons mit Funktionen
mainwindow_ui.actionCourseAdd.triggered.connect(show_edit_course_window)
mainwindow_ui.actionCourseView.triggered.connect(show_view_course_window)
mainwindow_ui.actionExamAdd.triggered.connect(show_edit_exam_window)
mainwindow_ui.actionExamView.triggered.connect(show_view_exam_window)
mainwindow_ui.actionResultView.triggered.connect(show_view_result_window)
mainwindow_ui.actionResultAdd.triggered.connect(show_edit_result_window)
mainwindow_ui.actionCourseRemove.triggered.connect(show_delete_course_window)
mainwindow_ui.actionExamRemove.triggered.connect(show_delete_exam_window)
mainwindow_ui.actionResultRemove.triggered.connect(show_delete_result_window)

edit_course_ui.save_button.clicked.connect(save_course)
edit_course_ui.add_student_button.clicked.connect(add_student_to_list)

edit_exam_ui.add_task_button.clicked.connect(add_task_to_list)
edit_exam_ui.save_button.clicked.connect(save_exam)

edit_result_ui.generate_table_button.clicked.connect(load_results_table)
edit_result_ui.save_button.clicked.connect(save_results)
edit_result_ui.print_button.clicked.connect(show_print_window)

print_ui.selectall_button.clicked.connect(select_all_students)
print_ui.printstudent_button.clicked.connect(print_students)
print_ui.printoverview_button.clicked.connect(print_analysis)

update_content()

mainwindow.show()

app.exec()
