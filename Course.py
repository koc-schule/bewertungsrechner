"""
Course Klasse
"""

class Course:
    def __init__(self, name: str, grading_scheme: str, student_names: list[str]) -> None:
        """
        Erstellen der Klasse

        Args:
            name: Name des Kurses
            grading_scheme: "sek1" oder "sek2" zum Festlegen des Bewertungssystems
            student_names: Liste mit den Schülernamen
        """
        self.course_name = name
        if grading_scheme in ('sek1', 'sek2'):
            self.grading_scheme = grading_scheme
        else:
            raise Exception('invalid grading scheme. Choose "sek1" or "sek2"')
        self.student_names = student_names

    def set_name(self, name: str) -> None:
        self.course_name = name

    def set_grading_scheme(self, grading_scheme: str) -> None:
        if grading_scheme in ('sek1', 'sek2'):
            self.grading_scheme = grading_scheme
        else:
            raise Exception('invalid grading scheme. Choose "sek1" or "sek2"')

    def set_student_names(self, studen_names: list[str]) -> None:
        self.student_names = studen_names

    def add_student(self, student_name: str) -> None:
        self.student_names.append(student_name)

    def remove_student(self, student_name: str) -> None:
        self.student_names.remove(student_name)




"""Test"""
if __name__ == '__main__':
    test_course = Course('LK11', 'sek', ['alice', 'bob'])
