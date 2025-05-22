"""Result Klasse"""
class Result:
    def __init__(self, results: list[dict], courses: list[Course], date: str, exam: Exam) -> None:
        self.courses = courses
        self.results = results
        self.date = date
        self.exam = exam

    def add_result(self, name: str, points_earned: int, percentage_earned: float, tasks: dict):
        output = {
            "name": name,
            "points_earned": points_earned,
            "percentage_earned": percentage_earned,
        }
        output = output | tasks
        self.results.append(output)
