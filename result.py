from course import Course
from exam import Exam
import math
"""Result Klasse"""

# PROZENTSÄTZE FÜR NOTENGRENZE
mark_percentage_borders_sek1 = {1: 0.95,
                                2: 0.80,
                                3: 0.60,
                                4: 0.40,
                                5: 0.20,
                                6: 0.00}
mark_percentage_borders_sek2 = {15: 0.95,
                                14: 0.90,
                                13: 0.85,
                                12: 0.80,
                                11: 0.75,
                                10: 0.70,
                                9: 0.65,
                                8: 0.60,
                                7: 0.55,
                                6: 0.50,
                                5: 0.45,
                                4: 0.40,
                                3: 0.3333,
                                2: 0.2666,
                                1: 0.20}



class Result:
    def __init__(self, courses: list[Course], results: list[dict], date: str, exam: Exam) -> None:
        """
        Anlegen eines Result Objekts

        Args:
            courses (list[Course]): Liste an Kursen, welche mit den Results zusammenhängen
            results (list[dict]): Liste an Ergebnisen der einzelnen Schüler
            date (str): Datum der Leistungskontrolle
            exam (Exam): Exam Vorlage mit maximalen Punkten und erreichbaren Punkten pro Aufgabe
        """
        self.courses = courses
        self.results = results
        self.date = date
        self.exam = exam

    def get_courses(self) -> list[Course]:
        return self.courses

    def set_courses(self, courses: list[Course]) -> None:
        self.courses = courses

    def get_results(self) -> list[dict]:
        return self.results

    def set_results(self, results: list[dict]) -> None:
        self.results = results

    def get_date(self) -> str:
        return self.date

    def set_date(self, date: str) -> None:
        self.date = date

    def get_exam(self) -> Exam:
        return self.exam

    def set_exam(self, exam: Exam) -> None:
        self.exam = exam

    def add_result(self, name: str, points_earned: int, percentage_earned: float, tasks: dict) -> None:
        """
        Hinzufügen eines einzelnen Ergebnisses zu self.results

        Args:
            name (str): Name des Schülers
            points_earned (int): Gesammt erreichte Punkte
            percentage_earned (float): Prozentsatz der gesammten Punktzahl der erreicht wurde
            tasks (dict): Dictionary an einzelnen Aufgaben mit den erreichten Punktzahlen
        """
        output = {
            "name": name,
            "points_earned": points_earned,
            "percentage_earned": percentage_earned,
        }
        output = output | tasks
        self.results.append(output)

    def quick_add_result(self, input_strs: list[str], exam: Exam, name_seperator_char: str = ",", task_seperator_char: str = " ") -> None:
        """
        Wandelt str in Ergebnisse um um die Eingabegeschwindigkeit zu erhöhen

        Args:
            input_strs: Liste mit den inputstrs pro schüler
            tasks: Dictionary mit Tasks aus Examobjekt

            (input_str: Name des Schülers, Punktzahlen mit " " getrennt)
        """
        for i in input_strs:
            student_name, earned_points = i.split(name_seperator_char)
            earned_points = earned_points.strip().split(task_seperator_char)

            for i in range(len(earned_points)):
                try:    earned_points[i] = int(i)
                except: pass

            total_points_earned = sum(earned_points)
            percentage = total_points_earned / exam.max_points * 100

            if len(earned_points) != len(exam.tasks):
                raise Warning(f'Ungültige Aufgabenanzahl bei Schüler {student_name}. Dieser Schüler wurde übersprungen.')
            else:
                # ergebnis deictionary erstellen
                student_result_dict = {key: earned_points.pop(0) for key in exam.tasks}

                self.add_result(student_name, total_points_earned, percentage, student_result_dict)

    
    def write_to_csv(self) -> None:
        """ Schreibt ein Result- Objekt in eine .csv-Datei um 
       
        Argumente: 
            result: Result
        """

        """Auswählen der Datei"""
        filename  = "results/" + str((self.get_courses())[0].course_name) + "_" + str((self.get_exam()).exam_name) + ".csv"
        file = open(filename,"w")

        """Erstellen der ersten Zeile der csv_datei (Spaltennamen)"""
        task_names_list = list(((self.get_exam()).tasks).keys())
        task_names = ""
        for key in task_names_list:
            task_names = task_names + str(key) + ", "
        column_name = "Name, Date, Percent, Points Earned, Points Possible, "  + task_names + "\n"
        file.write(column_name)

        """Eintragen der Ergebnisse für jeden Schüler"""
        for student in self.results:

            """gleichbleibende Einträge in Variablen speichern """
            student_name = student["name"] + ","
            exam_date = str(self.get_date()) + ","
            percentage_earned = str(student["percentage_earned"]) + ","
            points_earned = str(student["points_earned"]) + "," 
            max_points = str((self.get_exam()).max_points) + ","
            studentdata = student_name + exam_date + percentage_earned + points_earned + max_points 

            """Speichern der Punktzahlen je Aufgabe für einen Schüler """
            for task in list(((self.get_exam()).tasks).keys()):
                studentdata = studentdata + str(student[task]) + ","
            studentdata = studentdata + "\n"
            
            file.write(studentdata)  

    def gather_print_information(self, student_names: list[str])-> list[dict]:
        """ Sammelt Informationen über einen Schüler, welche eine Klausur geschrieben hat, damit diese (Informationen) anschließend gedruckt werden können
        Args:
        student_names: list[str]
        returns:
        list[dict]
        """
        students_information = []
        for student_name in student_names:
            """ bestimmen des Indizes des Schülers in self.results für einfacheren Zugriff"""
            studentindex = math.inf
            for i in range(len(self.results)):
                if (self.results[i])["name"] == student_name:
                    studentindex = int(i)
            student_information = {}

            """ Einfügen der nicht zu errechnenden Werte"""
            title = "Ergebnis " + (self.get_exam()).exam_name
            student_information["title"] = title
            student_information["date"] = self.get_date()
            student_information["teacher"] = "Herr Koch"
            student_information["subject"] = "Informatik "
            student_information["student_name"] = self.results[studentindex]["name"]
            student_information["points_earned"] = self.results[studentindex]["points_earned"]
            student_information["max_points"] =  (self.get_exam()).max_points

            """Berechnen der Note"""
            percentage_earned = self.results[studentindex]["percentage_earned"]
            grading_scheme = (self.courses[0]).grading_scheme
            points_earned = self.results[studentindex]["points_earned"]

            """ Berechnung der Note in der sek1 wird mithilfe der ereichten Punkte durchgeführt, um plus/minus bei einem Punkt darüber/darunter mit einzubeziehen."""
            if grading_scheme == "sek1":
                mark_1_points = math.ceil(mark_percentage_borders_sek1[1] * (self.get_exam()).max_points)
                mark_2_points = math.ceil(mark_percentage_borders_sek1[2] * (self.get_exam()).max_points)
                mark_3_points = math.ceil(mark_percentage_borders_sek1[3] * (self.get_exam()).max_points)
                mark_4_points = math.ceil(mark_percentage_borders_sek1[4] * (self.get_exam()).max_points)
                mark_5_points = math.ceil(mark_percentage_borders_sek1[5] * (self.get_exam()).max_points)

                if points_earned > mark_1_points:
                    mark = "1"
                elif points_earned == mark_1_points:
                    mark = "1-"
                elif points_earned == (mark_1_points - 1):
                    mark = "2+"
                elif points_earned > mark_2_points:
                    mark = "2"
                elif points_earned == mark_2_points:
                    mark = "2-"
                elif points_earned == (mark_2_points - 1):
                    mark = "3+"
                elif points_earned > mark_3_points:
                    mark = "3"
                elif points_earned == mark_3_points:
                    mark = "3-"
                elif points_earned == (mark_3_points - 1):
                    mark = "4+"
                elif points_earned > mark_4_points:
                    mark = "4"
                elif points_earned == mark_4_points:
                    mark = "4-"
                elif points_earned == (mark_4_points - 1):
                    mark = "5+"
                elif points_earned > mark_5_points:
                    mark = "5"
                elif points_earned == mark_5_points:
                    mark = "5-"
                elif points_earned == (mark_5_points - 1):
                    mark = "6+"
                else:
                    mark = "6"

            elif grading_scheme == "sek2":
                if percentage_earned >= mark_percentage_borders_sek2[15] * 100:
                    mark = "15"
                elif percentage_earned >= mark_percentage_borders_sek2[14] * 100:
                    mark = "14"
                elif percentage_earned >= mark_percentage_borders_sek2[13] * 100:
                    mark = "13"
                elif percentage_earned >= mark_percentage_borders_sek2[12] * 100:
                    mark = "12"
                elif percentage_earned >= mark_percentage_borders_sek2[11] * 100:
                    mark = "11"
                elif percentage_earned >= mark_percentage_borders_sek2[10] * 100:
                    mark = "10"
                elif percentage_earned >= mark_percentage_borders_sek2[9] * 100:
                    mark = "9"
                elif percentage_earned >= mark_percentage_borders_sek2[8] * 100:
                    mark = "8"
                elif percentage_earned >= mark_percentage_borders_sek2[7] * 100:
                    mark = "7"
                elif percentage_earned >= mark_percentage_borders_sek2[6] * 100:
                    mark = "6"
                elif percentage_earned >= mark_percentage_borders_sek2[5] * 100:
                    mark = "5"
                elif percentage_earned >= mark_percentage_borders_sek2[4] * 100:
                    mark = "4"
                elif percentage_earned >= mark_percentage_borders_sek2[3] * 100:
                    mark = "3"
                elif percentage_earned >= mark_percentage_borders_sek2[2] * 100:
                    mark = "2"
                elif percentage_earned >= mark_percentage_borders_sek2[1] * 100:
                    mark = "1"
                else:
                    mark = "0"
            student_information["mark"] = mark

            """Sammeln von Aufgabenname, erreichte Punkte und maximale Punkte pro Aufgabe"""
            tasks = []
            for task in list(((self.get_exam()).tasks).keys()):
                task_name = task
                points_earned = self.results[studentindex][task]
                max_points = (self.get_exam()).tasks[task]
                tasks.append((task_name, points_earned, max_points))
            student_information["tasks"] = tasks

            """Hinzufügen der Daten des Schülers zur Liste der Schülerdaten"""
            students_information.append(student_information)

        """ Rückgabe der gesammelten Informationen """
        return students_information

    def result_analysis(self) -> dict:
        """Sammelt die Daten für eine Auswertung
           Args:
           none
           returns:
           dict
        """
        analysis = {} 
        """ Sammeln aller zur Auswertung nötigen Informationen """
        result = self.gather_print_information()
        """Hinzufügen der bekannten/sich nicht ändernden Werte """
        analysis["title"] = result[0]["title"]
        analysis["date"] = result[0]["date"]
        analysis["teacher"] = result[0]["teacher"]
        analysis["subject"] = result[0]["subject"]
        analysis["max_points"] = (self.get_exam()).max_points 


        """ Hinzufügen der Noten jedes Schülers """
        marks = []
        for student in result:
            student_name = student["student_name"]
            student_mark = student["mark"]
            marks.append((student_name, student_mark))
        analysis["marks"] = marks

        """ Hinzufügen der im Durchschnitt erreichten Punkte pro Aufgabe """
        tasks = []
        for task in list(((self.get_exam()).tasks).keys()):
            task_name = task 
            max_points = (self.get_exam()).tasks[task] 
            """ Berechnung der durchschnittlichen Punkte pro Aufgabe """
            points_sum = 0
            students_counter = len(result)
            for student in result:
                task_index = 0
                for i in range (len(list(((self.get_exam()).tasks).keys()))):
                    if student["tasks"][i][0] == task_name: taskindex = i 
                points_sum += student["tasks"][taskindex][1]
            average_points = points_sum / students_counter 
            tasks.append((task_name, average_points, max_points))
        analysis["tasks"] = tasks

        """ Berechnen des Notendurchschnitts """
        if (self.courses[0]).grading_scheme == "sek2":
            marks_sum = 0
            students_counter = len(result)
            for student in result:
                marks_sum += int(student["mark"])
            average_mark = marks_sum / students_counter
            analysis["average"] = average_mark

        elif (self.courses[0]).grading_scheme == "sek1":
            """ Erstellen einer neuen Liste aller Noten ohne Minus und Plus """
            marks = []
            for student in result:
                marks.append(int(student["mark"][0]))

            students_counter = len(result)
            marks_sum = 0
            for mark in marks: 
                marks_sum += mark
            average_mark = marks_sum / students_counter
            analysis["average"] = average_mark

        """ Zurückgeben der gesammelten Daten"""
        return analysis
