import json
from exam import Exam
from course import Course

def exam_to_json(exam: Exam) -> None:
    """
    Saves a Exam object to JSON file 

    Args:
        exam (Exam): The Exam object to be saved
    """
    data = {
        "name": exam.exam_name,
        "notes": exam.notes,
        "max_points": exam.max_points,
        "tasks": exam.tasks
    }
    with open(f'files/exams/exam_{exam.exam_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def json_to_exam(name: str) -> Exam:
    """
    Generates a Exam object from a JSON file

    Args:
        name (str): The name specified in the filename (exam_[name].json)

    Returns:
        generated_exam (Exam): The Exam object generated from the JSON file
    """
    with open(f'files/exams/exam_{name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        generated_exam = Exam(data["name"], data["notes"])
        generated_exam.max_points = data["max_points"]
        generated_exam.tasks = data["tasks"]
    return generated_exam

def course_to_json(course: Course) -> None:
    """
    Saves a Course object to JSON file 

    Args:
        course (Course): The Course object to be saved
    """
    data = {
        "name": course.course_name,
        "grading_scheme": course.grading_scheme,
        "student_names": course.student_names
    }
    with open(f'files/courses/course_{course.course_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def json_to_course(name: str) -> Course:
    """
    Generates a Course object from a JSON file

    Args:
        name (str): The name specified in the filename (course_[name].json)

    Returns:
        generated_course (Course): The Course object generated from the JSON file
    """
    with open(f'files/courses/course_{name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        generated_course = Course(data["name"], data["grading_scheme"], data["student_names"])
    return generated_course
