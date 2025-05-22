"""Result Klasse"""
class Result:
    def __init__(self, results: list[dict], courses: list[Course], date: str, exam: Exam) -> None:
        self.courses = courses
        self.results = results
        self.date = date
        self.exam = exam


