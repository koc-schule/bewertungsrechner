"""importieren der Result-Klasse aus dem parent-directory"""
import sys
import os
import utils.csv
from course import Course
from result import Result
from exam import Exam

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


def course_object_to_csv_file(course: Course) -> None:
    """
    Schreibt eine .csv-Datei (Namensformat: course_kursname.csv) für einen Course

    Args:
        course (Course): Einzulesendes Course-Objekt
    """

    content = str(course.course_name + "\n" + course.grading_scheme + "\n")
    for student in course.student_names:
        content = content + (student + ";")

    content = content[:-1]

    path = os.getcwd() + "/csv_files/course_" + course.course_name + ".csv"

    """Format: course_name \n grading_scheme \n student_names (Schüler mit ';' getrennt)"""
    utils.csv.write_csv(path, content)


def exam_object_to_csv_file(exam: Exam) -> None:
    """
    Schreibt eine .csv-Datei (Namensformat: exam_examname.csv) aus einem Exam-Objekt

    Args:
        exam (Exam): Einzulesendes Exam-Objekt
    """

    """Format von exam.notes wird angepasst"""
    notes_polished = exam.notes.replace("\n", ";")
    content = str(exam.exam_name + "\n" + notes_polished + "\n" + str(exam.tasks))

    path = os.getcwd() + "/csv_files/exam_" + exam.exam_name + ".csv"

    """Format: name \n notes (mit ';' getrennt \n max_points \n taks (Format: task:Punktzahl"""
    utils.csv.write_csv(path, content)


def result_object_to_csv_file(result: Result) -> None:
    """ Schreibt ein Result-Objekt in eine .csv-Datei um
       
       Args:
            result (Result): Einzulesendes Result-Objekt
   """

    """Auswählen der Datei"""
    filename = "./csv_files/" + str((result.get_exam()).exam_name) + ".csv"
    file = open(filename, "w")

    """Erstellen der ersten Zeile der csv_datei (Spaltennamen)"""
    task_names_list = list(((result.get_exam()).tasks).keys())
    task_names = ""
    for key in task_names_list:
        task_names = task_names + str(key) + ", "
    column_name = "Name, Date, Percent, Points Earned, Points Possible, " + task_names + "\n"
    file.write(column_name)

    """Eintragen der Ergebnisse für jeden Schüler"""
    for student in result.results:

        """gleichbleibende Einträge in Variablen speichern """
        student_name = student["name"] + ","
        exam_date = str(result.get_date()) + ","
        percentage_earned = str(student["percentage_earned"]) + ","
        points_earned = str(student["points_earned"]) + ","
        max_points = str((result.get_exam()).max_points) + ","
        studentdata = student_name + exam_date + percentage_earned + points_earned + max_points

        """Speichern der Punktzahlen je Aufgabe für einen Schüler """
        for task in list(((result.get_exam()).tasks).keys()):
            studentdata = studentdata + str(student[task]) + ","
        studentdata = studentdata + "\n"

        file.write(studentdata)
