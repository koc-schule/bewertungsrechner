"""Exam Klasse"""

class Exam:
    def __init__(self, name: str, notes) -> None:
        """
        Erstellen der eines Exam Objekts

        Args:
            name (str): Name des Tests
            notes (str): Benutzerdefinierte Notizen 
        """
        self.name = name
        self.notes = notes
        self.max_points = 0
        self.tasks = []

    def set_name(self, name: str) -> None:
        """
        Ändern der self.name Variable

        Args:
            name (str): Neuer Wert von self.name
        """
        new_name = name
    
    def add_note(self, notes_to_add: str) -> None:
        """
        Hinzufügen einer Notiz zu self.notes

        Args: 
            notes_to_add (str): Hinzuzufügender Wert zu self.notes
        """
        self.notes.append(notes_to_add)

    def clear_notes(self) -> None:
        """
        Setzt den Wert von self.notes auf "" zurück
        """
        self.notes = ""
    
    def update_max_points(self) -> None:
        """
        Berechnet den Wert von self.max_points
        """
        self.max_points = 0
        for item in self.tasks:
            self.max_points += item["points"]

    def add_task(self, task_point_pairs: str) -> None:
        """
        Fügt eine Aufgabe zu self.tasks hinzu 
        Dabei werden diese als Dictionary in einer Liste gespeichert
        Format: {"task_number": [Nummer der Aufgabe], "points": [maximale Punktzahl]}

        Args:
            task_point_pairs (str): In Format [Nummer der Aufgabe]:[maximale Punktzahl]
                                    bsp: 1:10, 2.1:5, 2.2:5
        """
        for task_point_pair in task_point_pairs.split(","):
            task, points = task_point_pair.strip().split(":")
            self.tasks.append({"task_number": task, "points": int(points)})
        self.update_max_points()

    def remove_task(self, task_number: str) -> None:
        """
        Entfernen einer Aufgabe, spezifiziert durch die Aufgaben-Nummer
        Anschießend wird self.max_points aktualisiert  

        Args:
            task_number (str): Nummer der Aufgabe, welche gelöscht werden soll
        """
        for task in self.tasks:
            if task["task_number"] == task_number:
                index = self.tasks.index(task)
                self.tasks.pop(index)
        self.update_max_points()


"""Test"""
exam1 = Exam("Test_Exam", "")
exam1.add_task("1:10, 2.1:5, 2.2:5")
exam1.remove_task("1")
print(exam1.max_points)
