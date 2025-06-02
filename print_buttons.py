from __future__ import annotations
from printer import printer_templates
from utils import parser
import random
import time
import gui

def print_students():
    result = parser.csv_to_result(gui.print_ui.resultname_label.text())
    list_schueler = None # liste der schüler einfügen
    list_infos = result.gather_print_information(list_schueler)
    for i in list_infos:
        printer_templates.PrinterTemplates.student_result_receipt(**i)

def print_analysis():
    result = parser.csv_to_result(gui.print_ui.resultname_label.text())
    infos = result.result_analysis()
    printer_templates.PrinterTemplates.course_result_receipt(**infos)