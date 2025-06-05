"""Exam Klasse"""

class Exam:
    def __init__(self, name: str, notes: str) -> None:
        """
        Erstellen eines Exam Objekts

        Args:
            name (str): Name des Tests
            notes (str): Benutzerdefinierte Notizen 
        """
        self.exam_name = name
        self.notes = notes
        self.max_points = 0
        self.tasks = {}

    def set_name(self, name: str) -> None:
        """
        Ändern der self.name Variable

        Args:
            name (str): Neuer Wert von self.name
        """
        self.exam_name = name
    
    def add_note(self, notes_to_add: str) -> None:
        """
        Hinzufügen einer Notiz zu self.notes

        Args: 
            notes_to_add (str): Hinzuzufügender String zu self.notes
        """
        if self.notes == '':
            self.notes += notes_to_add
        else:
            self.notes += '\n' + notes_to_add

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
        for task_name in self.tasks:
            self.max_points += self.tasks[task_name]

    def add_task(self, task_name: str, task_points: int) -> None:
        """
        Fügt eine Aufgabe zum Exam hinzu

        Args:
            task_name (str): Name der Aufgabe
            tast_points (int): Punktzahl der Aufgabe
        """
        self.tasks[task_name] = task_points
        self.update_max_points()

    def remove_task(self, task_name: str) -> None:
        """
        Entfernt eine Aufgabe

        Args:
            task_name (str): Name der Aufgabe
        """
        self.max_points -= self.tasks.pop(task_name)

    def quick_add_tasks(self, input_string: str,
                        names_given: bool = False,
                        numbering_scheme: str = 'task:numbersubtask:letter)',
                        task_seperator_char: str = ',',
                        subtask_seperator_char: str = ' ',
                        name_seperator_char: str = ':') -> None:
        """
        Erstellt Aufgaben aus quick-input-string

        Args:
            input_string (str): aufgaben mit ',' getrennt, Unteraufgaben mit ' ', (bzw. angegebenen Zeichen)
                            Nur Punktzahlen, falls names_given=True stattdessen Name:Punkzahl (bzw. anderes Zeichen)
                            für jede (Unter-)Aufgabe
                            Bsp: 'a1:5\n a2.2:4 a2.2:5\n a3:8'
                               '5\n 3 4 2\n 2 2'
                          
            names_given (bool): True wenn Namen angegeben werden sollen
            numbering_scheme (str): falls names_given=False Schema der automatischen Aufgabennummerierung
                              'task:' nummerierung der aufgaben nach angegebenen muster
                              'subtask:' nummerierung der unteraufgaben nach angegebenen muster
                              muster: 'number' wird mit nummer ersetzt, 'letter' mit buchstabe

            task_seperator_char (str): Hier kann abweichendes Zeichen zum Trennen der Aufgaben angegeben werden
            subtask_seperator_char (str): Analog zu task_seperator_char
            name_seperator_char (str): Analog zu task_seperator_char
        """
        tasks = input_string.strip().split(task_seperator_char)


        """ Aufgabennummerierung konfigurieren """
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        """ Gibt für Buchstaben den nächsten (nach z wieder a) und für Zahl ebenfalls die nächste an """
        next_numbering_char = lambda x: alphabet[(alphabet.index(x) + 1) % len(alphabet)] if type(x) == str else x + 1

        if 'subtask:number' in numbering_scheme:
            start_subtaskchar = 1
            next_subtaskchar = 1
            numbering_scheme = numbering_scheme.replace('subtask:number', 'subtask')
        elif 'subtask:letter' in numbering_scheme:
            start_subtaskchar = 'a'
            next_subtaskchar = 'a'
            numbering_scheme = numbering_scheme.replace('subtask:letter', 'subtask')

        if 'task:number' in numbering_scheme:
            next_taskchar = 1
            numbering_scheme = numbering_scheme.replace('task:number', 'task')
        elif 'task:letter' in numbering_scheme:
            next_taskchar = 'a' 
            numbering_scheme = numbering_scheme.replace('task:letter', 'task')


        """ Aufgaben anlegen """
        for task in tasks:
            task = task.strip()

            """ Fall 1: hat Unteraufgaben - Fall 2: keine Unteraufgaben"""
            if ' ' in task and names_given:
                for subtask in task.split(subtask_seperator_char):
                    self.add_task(subtask.split(name_seperator_char)[0], int(subtask.split(name_seperator_char)[1]))
            elif ' ' in task and not names_given:
                for subtask in task.split(subtask_seperator_char):
                    self.add_task(
                        numbering_scheme.replace('subtask', str(next_subtaskchar)).replace('task', str(next_taskchar)),
                        int(subtask)
                    )
                    """ nächstes unteraufabenzeichen """
                    next_subtaskchar = next_numbering_char(next_subtaskchar)


            elif not subtask_seperator_char in task and names_given:
                self.add_task(task.split(name_seperator_char)[0], int(task.split(name_seperator_char)[1]))
            elif not ' ' in task and not names_given:
                self.add_task(
                    numbering_scheme.replace('subtask', '').replace('task', str(next_taskchar)),
                    int(task)
                )

            """ nächstes Aufgabenzeichen; erste Unteraufgabenzeichen setzen """
            next_taskchar = next_numbering_char(next_taskchar)
            next_subtaskchar = start_subtaskchar

        self.update_max_points()




"""Test"""
if __name__ == '__main__':
    exam1 = Exam("Test_Exam", "")

    exam1.quick_add_tasks('eins:1\nzweiA:2 zweiB:3 zweiC:4\ndreiA:3 dreiB:24', names_given=True)

    print(exam1.tasks)
