from course import Course
from exam import Exam
import math
"""Result Klasse"""


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
            percentage_earned = str(round(student["percentage_earned"])) + ","
            points_earned = str(student["points_earned"]) + "," 
            max_points = str((self.get_exam()).max_points) + ","
            studentdata = student_name + exam_date + percentage_earned + points_earned + max_points 

            """Speichern der Punktzahlen je Aufgabe für einen Schüler """
            for task in list(((self.get_exam()).tasks).keys()):
                studentdata = studentdata + str(student[task]) + ","
            studentdata = studentdata + "\n"
            
            file.write(studentdata)  
    def gather_print_information(self, student_name: str)-> dict:
        """ Sammelt Informationen über einen Schüler, welche eine Klausur geschrieben hat, damit diese (Informationen) anschließend gedruckt werden können
        Args:
        student_name:str
        returns:
        dict
        """
        
        """ bestimmen des Indizes des Schülers in self.results für einfacheren Zugriff"""
        studentindex=0
        for i in range(len(self.results)):
            if (self.results[1])["name"] == student_name:
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
            mark_1_points = math.ceil(0.95*(self.get_exam()).max_points)
            mark_2_points = math.ceil(0.8*(self.get_exam()).max_points)
            mark_3_points = math.ceil(0.6*(self.get_exam()).max_points)
            mark_4_points = math.ceil(0.4*(self.get_exam()).max_points)
            mark_5_points = math.ceil(0.8*(self.get_exam()).max_points)
            
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
            mark_15_percentage = 95
            mark_14_percentage = 90
            mark_13_percentage = 85
            mark_12_percentage = 80
            mark_11_percentage = 75
            mark_10_percentage = 70
            mark_9_percentage = 65
            mark_8_percentage = 60
            mark_7_percentage = 55
            mark_6_percentage = 50
            mark_5_percentage = 45
            mark_4_percentage = 40
            mark_3_percentage = 33.33
            mark_2_percentage = 26.66
            mark_1_percentage = 20
            if percentage_earned >= mark_15_percentage: 
                mark = "15"
            elif percentage_earned >= mark_14_percentage: 
                mark = "14"
            elif percentage_earned >= mark_13_percentage: 
                mark = "13"
            elif percentage_earned >= mark_12_percentage: 
                mark = "12"
            elif percentage_earned >= mark_11_percentage: 
                mark = "11"
            elif percentage_earned >= mark_10_percentage: 
                mark = "10"
            elif percentage_earned >= mark_9_percentage: 
                mark = "9"
            elif percentage_earned >= mark_8_percentage: 
                mark = "8"
            elif percentage_earned >= mark_7_percentage: 
                mark = "7"
            elif percentage_earned >= mark_6_percentage: 
                mark = "6"
            elif percentage_earned >= mark_5_percentage: 
                mark = "5"
            elif percentage_earned >= mark_4_percentage: 
                mark = "4"
            elif percentage_earned >= mark_3_percentage: 
                mark = "3"
            elif percentage_earned >= mark_2_percentage: 
                mark = "2"
            elif percentage_earned >= mark_1_percentage: 
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
        
        """ Rückgabe der gesammelten Informationen """
        return student_information
    def gather_print_information(self) -> list[dict]:
        """ Sammelt Informationen über die Kurse, welche eine Klausur geschrieben haben, damit diese (Informationen) anschließend gedruckt werden können
        Args:
        none
        returns:
        list[dict]
        """
        students_information=[]
        """for-loop, welcher alle schüler der kurse durchgeht""" 
        for student in self.results:
            student_information={}
            """ Einfügen der nicht zu errechnenden Werte"""
            title = "Ergebnis " + (self.get_exam()).exam_name
            student_information["title"] = title
            student_information["date"] = self.get_date()
            student_information["teacher"] = "Herr Koch"
            student_information["subject"] = "Informatik "
            student_information["student_name"] = student["name"]
            student_information["points_earned"] = student["points_earned"]
            student_information["max_points"] =  (self.get_exam()).max_points

            """Berechnen der Note"""
            percentage_earned = student["percentage_earned"]
            grading_scheme = (self.courses[0]).grading_scheme
            points_earned = student["points_earned"]

            """ Berechnung der Note in der sek1 wird mithilfe der ereichten Punkte durchgeführt, um plus/minus bei einem Punkt darüber/darunter mit einzubeziehen."""
            if grading_scheme == "sek1":
                mark_1_points = math.ceil(0.95*(self.get_exam()).max_points)
                mark_2_points = math.ceil(0.8*(self.get_exam()).max_points)
                mark_3_points = math.ceil(0.6*(self.get_exam()).max_points)
                mark_4_points = math.ceil(0.4*(self.get_exam()).max_points)
                mark_5_points = math.ceil(0.8*(self.get_exam()).max_points)

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
                mark_15_percentage = 95
                mark_14_percentage = 90
                mark_13_percentage = 85
                mark_12_percentage = 80
                mark_11_percentage = 75
                mark_10_percentage = 70
                mark_9_percentage = 65
                mark_8_percentage = 60
                mark_7_percentage = 55
                mark_6_percentage = 50
                mark_5_percentage = 45
                mark_4_percentage = 40
                mark_3_percentage = 33.33
                mark_2_percentage = 26.66
                mark_1_percentage = 20
                if percentage_earned >= mark_15_percentage:
                    mark = "15"
                elif percentage_earned >= mark_14_percentage:
                    mark = "14"
                elif percentage_earned >= mark_13_percentage:
                    mark = "13"
                elif percentage_earned >= mark_12_percentage:
                    mark = "12"
                elif percentage_earned >= mark_11_percentage:
                    mark = "11"
                elif percentage_earned >= mark_10_percentage:
                    mark = "10"
                elif percentage_earned >= mark_9_percentage:
                    mark = "9"
                elif percentage_earned >= mark_8_percentage:
                    mark = "8"
                elif percentage_earned >= mark_7_percentage:
                    mark = "7"
                elif percentage_earned >= mark_6_percentage:
                    mark = "6"
                elif percentage_earned >= mark_5_percentage:
                    mark = "5"
                elif percentage_earned >= mark_4_percentage:
                    mark = "4"
                elif percentage_earned >= mark_3_percentage:
                    mark = "3"
                elif percentage_earned >= mark_2_percentage:
                    mark = "2"
                elif percentage_earned >= mark_1_percentage:
                    mark = "1"
                else:
                    mark = "0"
            student_information["mark"] = mark

            """Sammeln von Aufgabenname, erreichte Punkte und maximale Punkte pro Aufgabe"""
            tasks = []
            for task in list(((self.get_exam()).tasks).keys()):
                task_name = task
                points_earned = student[task]
                max_points = (self.get_exam()).tasks[task]
                tasks.append((task_name, points_earned, max_points))
            student_information["tasks"] = tasks

            """Hinzufügen der Einträge für einen Schüler zur Liste aller Schüler """
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
