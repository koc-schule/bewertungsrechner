from Course import Course
from Exam import Exam

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
