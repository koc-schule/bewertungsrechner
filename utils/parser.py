import csv
import utils.csv
from exam import Exam
from course import Course
from result import Result
from utils.json_parser import *
import os
import sys
"""current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)"""

def results_csv_file_to_object(csv_name: str, new_csv: bool) -> list[dict]:
    """erstellt eine Liste, in der dictionaries gespeichert werden, die die ergebnisse enthalten
        Args:
            csv_name: Name der .csv-Datei
            new_csv: gibt an, ob es sich um eine neue oder alte Datei handelt
        Returns:
            list[dict], in der alle Schüler und deren Ergebnisse stehen
        """
    results = []
    filename = "resources/results/" + csv_name
    file = open(filename, "r")
    i = 1

    while True:
        try:
            row = file.readline()
            if new_csv:
                row = remove_unimportant_data(row)
            else:
                row = row[:-1]
            results.append({
                row[:row.index(",")].replace("ï»¿", ""): row[row.index(",") + 1:].replace("\n", "")
            })
            i += 1
        except:
            break

    return results



def remove_unimportant_data(row: str) -> str:
    """löscht aus einer Zeile der Ergebnisse unnötige Daten heraus: starttime, endtime, time
    Args:
        row: Zeile, aus der Start-, End- und Gesamtzeit entfernt werden
    """
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

def csv_to_result(name: str) -> Result:
    """
    Erzeugt ein Result object aus einer CSV tabelle
    """
    csv_path = f"resources/results/{name}.csv"
    results = []
    date = ""
    course_name, exam_name = name.strip().split("_")
    course = json_to_course(course_name)
    exam = json_to_exam(exam_name)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        task_names = [col.strip() for col in header[5:] if col.strip()]
        for row in reader:
            if not row or not row[0].strip():
                continue
            name = row[0].strip()
            date = row[1].strip()
            percent = float(row[2].strip())
            points_earned = int(row[3].strip())
            # points_possible = int(row[4].strip())  # Not used, taken from exam
            tasks = {}
            for i, task in enumerate(task_names):
                if 5 + i < len(row) and row[5 + i].strip():
                    tasks[task] = int(row[5 + i].strip())
                else:
                    tasks[task] = 0
            result_entry = {
                "name": name,
                "points_earned": points_earned,
                "percentage_earned": percent,
                **tasks
            }
            results.append(result_entry)
    return Result([course], results, date, exam)

# print(results_csv_file_to_object("quiz_13965756.csv", True))