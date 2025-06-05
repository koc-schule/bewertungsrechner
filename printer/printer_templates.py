from __future__ import annotations
from . import *
from . import printer_library
from .printer_library import *

class PrinterTemplates(PrinterLibrary):
    """
    Bibliothek mit möglichen Templates für den Druck von Kassenbons.
    Über diese Klassen werden die statischen Methoden für die Grundlegenden Templates gestartet.
    """
    #region Access
    printer: PrinterTemplates = None
    #endregion
    
    def __init__(self) -> None:
        """
        Initialisiert die `PrinterLibrary` die die spezifischen Operationen zur Verfügung stellt.
        """
        super().__init__()
    
    @staticmethod
    def simple_receipt(**kwargs) -> None:
        """
        Ignore this it's just useless stuff right now
        """
        log.log(str(type(PrinterTemplates.printer)))
        PrinterTemplates.printer.activate("write_text", text=kwargs["title"])
    
    @staticmethod
    def student_result_receipt(**kwargs) -> None:
        """
        Druckt einen Kassenbon für die Ergebnisse einer `Exam` für einen Schüler.

        Args:
            title (str): Name der `Exam`
            date (str): Datum der `Exam`
            teacher (str): Lehrer
            subject (str): Fach (evtl. vernachlässigbar)
            student (str): Name des Schülers
            tasks (list[tuple[str, int, int]]): Aufgaben der `Exam` mit erreichten und maximalen Punkten
            points (int): Erreichte gesamte Punktzahl
            max_points (int): Maximal mögliche Punktzahl
            mark (int): Note (1-6 oder 0-15)
        """
        # Schreibt den Titel der Klausur
        PrinterTemplates.printer.activate("write_text", text=kwargs["title"])
        
        # Schreibt Tabelle mit Datum, Lehrer und Fach
        header_table = [
            ("Datum:", kwargs["date"]),
            ("Lehrer:", kwargs["teacher"]),
            ("Fach:", kwargs["subject"])
        ]
        PrinterTemplates.printer.activate("table_2", content=header_table)
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        # Tabelle mit Namen des Schülers        
        name_table = [
            ("Name:", kwargs["student_name"])
        ]
        PrinterTemplates.printer.activate("table_2", content=name_table)
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        # Tabelle mit Aufgaben und den jeweils erreichten Punkten und Kopfzeile
        kwargs["tasks"].insert(0, ("Aufgabe", "Erreicht", "Maximal"))
        PrinterTemplates.printer.activate("table_3", content=kwargs["tasks"], ratio=(12, 9, 8))
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        if "average" in kwargs:
            PrinterTemplates.printer.activate("table_2", content=[("Durchschnitt:", kwargs["average"])], ratio=(26, 4))
        
        # Gesamte Punkte und Note als Tabelle        
        PrinterTemplates.printer.activate("table_3", content=[("Punkte:", kwargs["points_earned"], kwargs["max_points"])], ratio=(19, 5, 5))
        PrinterTemplates.printer.activate("table_2", content=[("Note:", kwargs["mark"])], ratio=(26, 4))
        
        # Platz für Unterschrift
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("break")
            
    @staticmethod
    def course_result_receipt(**kwargs) -> None:
        """
        Druckt einen Kassenbon für die Ergebnisse einer `Exam` für einen `Course`.

        Args:
            title (str): Name der `Exam`
            date (str): Datum der `Exam`
            teacher (str): Lehrer
            subject (str): Fach (evtl. vernachlässigbar)
            results (list[tuple[str, int, int]]): Noten der Schüler (evtl. auch mit erreichten Punkten oder so)
            max_points (int): Maximal mögliche Punktzahl
        """
        # Schreibt den Titel der Klausur
        PrinterTemplates.printer.activate("write_text", text=kwargs["title"])
        
        # Schreibt Tabelle mit Datum, Lehrer und Fach
        header_table = [
            ("Datum:", kwargs["date"]),
            ("Lehrer:", kwargs["teacher"]),
            ("Fach:", kwargs["subject"])
        ]
        PrinterTemplates.printer.activate("table_2", content=header_table)
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        # Tabelle mit Aufgaben und den durchschnittlich erreichten Punkten und Kopfzeile        
        kwargs["tasks"].insert(0, ("Aufgabe", "Durchschnitt", "Maximal"))
        PrinterTemplates.printer.activate("table_3", content=kwargs["tasks"], ratio=(9, 12, 8))
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        # Tabelle mit Aufgaben und den jeweils erreichten Punkten und Kopfzeile        
        kwargs["marks"].insert(0, ("Schueler", "Note"))
        PrinterTemplates.printer.activate("table_2", content=kwargs["marks"], ratio=(26, 4))
        
        # Trennstrich
        PrinterTemplates.printer.activate("break")
        PrinterTemplates.printer.activate("line")
        PrinterTemplates.printer.activate("break")
        
        if "average" in kwargs:
            PrinterTemplates.printer.activate("table_2", content=[("Durchschnitt:", kwargs["average"])], ratio=(26, 4))
    
    @staticmethod
    def break_line() -> None:
        """
        Druckt einen Trennstrich zwischen zwei Bons.
        """
        # Trennstrich
        PrinterTemplates.printer.activate("line")
        
        
PrinterTemplates.printer = PrinterTemplates()