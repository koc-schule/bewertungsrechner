from __future__ import annotations
from printer import printer_templates
import random
import time

printer_templates.PrinterTemplates.student_result_receipt(
    title="Ergebnis Klausur",
    date=time.strftime("%Y-%m-%d", time.localtime(time.time())),
    teacher="Herr Koch",
    subject="Informatik",
    student="oma sohn",
    tasks=[
        ("1.", 5, 7),
        ("2.", 3, 3),
        ("Z.", 0, 1)
    ],
    points=8,
    max_points=10,
    mark=12,
    average=13.5
)

printer_templates.PrinterTemplates.course_result_receipt(
    title="Ergebnis Klausur",
    date=time.strftime("%Y-%m-%d", time.localtime(time.time())),
    teacher="Herr Koch",
    subject="Informatik",
    results=[
        ("student 1", 5),
        ("student 2", 3),
        ("student 3", 0)
    ],
    max_points=10,
    average=13.5
)