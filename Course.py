"""Course Klasse"""
class Course:
    def __init__(self, name: str, grading_scheme: str) -> None:
        self.course_name = name
        if grading_scheme in ('sek1', 'sek2'):
            self.grading_scheme = grading_scheme

