import csv
import utils.csv
from Course import Course
import os


def course_csv_file_to_object(name: str) -> Course:
    """
    Einlesen der .csv-Dateien für Klassen

    Args:
        name (str): Name des Kurses (ohne .csv)

    Returns:
        Course | bool: Course-Objekt oder False, wenn Objekt nicht angelegt werden kann
    """

    path = os.getcwd() + "/csv_files/" + name + ".csv"
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


"""Test für Course-Dateien Lesen und Schreiben"""
if __name__ == '__main__':
    test_course = Course('LK11', 'sek2', ['Nachname1, Vorname1', 'Nachname2, Vorname2'])
    course_object_to_csv_file(test_course)
    test_course_2 = course_csv_file_to_object("course_LK11")


"""
Aus einer .csv-Datei werden Ergebnisse herausgelesen und in einer list[dict] zurückgegeben
"""


def results_csv_file_to_object(csv_name: str) -> list[dict]:
    """erstellt eine Liste, in der dictionaries gespeichert werden, die die ergebnisse enthalten"""
    results = []
    file = open(csv_name, "r")
    i = 1
    while True:
        try:
            row = file.readline()
            row = remove_unimportant_data(row)
            results.append({
                row[:row.index(",")].replace("ï»¿", ""): row[row.index(",") + 1:].replace("\n", "")
            })
            i += 1
        except:
            break

    return results


def remove_unimportant_data(row: str) -> str:
    """löscht aus einer Zeile der Ergebnisse unnötige Daten heraus: starttime, endtime, time"""
    counter = 0
    for i in range(len(row)):
        if row[i] == ",":
            counter += 1
        if counter == 1:
            start_index = i
            counter += 1
        elif counter == 5:
            row = row[:start_index] + row[i:]
            return row

print(results_csv_file_to_object("quiz_13965756.csv"))