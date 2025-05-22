"""
Beschreibung
"""
import csv

import utils.csv
from Course import Course
import os


def course_csv_file_to_object(name: str) -> list[str]:
    """
    Einlesen der .csv-Dateien für Klassen

    Args:
        name (str): Name des Kurses
        
    Returns:
        Course: Course-Objekt
    """

    path = os.getcwd() + "/csv_files/" + name + ".csv"

    """Jede Zeile der Datei wird in ein Attribut umgewandelt"""
    all_lines = utils.csv.read_csv_lines(path)
    return Course(all_lines[0][:-1], all_lines[1][:-1], all_lines[2].split(";"))

def course_object_to_csv_file(course: Course) -> None:
    """
    Schreibt eine .csv-Datei für einen Course

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



"""Test"""
if __name__ == '__main__':
    test_course = Course('LK11', 'sek1', ['alice', 'bob'])
    course_object_to_csv_file(test_course)
    test_course_2 = course_csv_file_to_object("course_LK11")
    print(test_course_2)
