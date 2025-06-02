"""
Bitte nicht eigenständig bearbeiten, hier soll die generelle Klassenstruktur etc. pp hin.
"""
from typing import Callable
from course import Course
from exam import Exam


courses = []
exams = []
results = []


def terminal_user_interface() -> None:
    """
    Software Steuerung über das Terminal
    """
    def print_heading(heading_text: str, is_subheading: bool=False) -> None:
        if not is_subheading:
            heading_text = ' '.join(list(heading_text.upper()))

        print('=' * 50)
        if len(heading_text) <= 50:
            #           Zentrierung
            print(' ' * int((50 - len(heading_text)) / 2) + heading_text)
        else:
            print(heading_text)
        print('=' * 50, '\n')

    def print_menu(menu_items: list[tuple[str, Callable]]) -> None:
        for i in range(len(menu_items)):
            print(f'     ({i + 1}) {menu_items[i][0]}')

        auswahl = ''
        while type(auswahl) != int:
            auswahl = input('\nGeben Sie die Nummer des gewüschten Menupunktes ein: ').strip()
            try:    auswahl = int(auswahl)
            except: pass

        menu_items[auswahl - 1][1]()

    def print_numbered_list(list_heading: str, list_items: list) -> None:
        print('     ' + list_heading)
        for i in range(len(list_items)):
            print(f'          [{i + 1}] {list_items[i]}')

        if len(list_items) == 0:
            print('          keine')
        print()



    def start_gui() -> None:
        print('GUI noch nicht implementiert')

    def course_window() -> None:
        """Kursverwaltungsmenu"""

        def show_course() -> None:
            print('Noch nicht implementiert')

        def add_course() -> None:
            """Neune Kurs anlegen und zum Kursmenu zurückkehren"""
            print('\nNeuen Kurs anlegen\n')
            course_name = input('Kursname: ')
            grading_scheme = 'sek1'
            if input('Bewertungssystem ist auf "sek1" gesetzt;\n'
                     'Geben Sie irgendetwas ein um zu "sek2" zu wechseln: ') != '':
                grading_scheme = 'sek2'
            student_names = input('Schülernamen (getrennt mit ","): ').split(',')

            courses.append(Course(course_name, grading_scheme, student_names))

            course_window()

        def edit_course():
            print('Noch nicht implementiert')

        def delete_course():
            """Kurs löschen und zum Kursmenu zurückkehren"""
            print('\n Kurs löschen\n')
            print_numbered_list('Bestehende Kurse', [i.course_name for i in courses])

            course_index = ''
            while type(course_index) != int:
                course_index = input('Geben Sie die Nummer des zu löschenden Kurses ein: ')
                try:
                    courses.pop(int(course_index) - 1)
                    break
                except: pass

            course_window()

        # Kursfenster
        print_heading('Kursverwaltung', is_subheading=True)

        print_numbered_list('Bestehende Kurse', [i.course_name for i in courses])



        course_window_menu_items = [('Kursdaten anzeigen', show_course)
                                    ('Kurs anlegen', add_course),
                                    ('Kurs bearbeiten', edit_course),
                                    ('Kurs löschen', delete_course),
                                    ('Zurück zum Hauptmenu', main_window)]
        print_menu(course_window_menu_items)

    def exam_window() -> None:
        """Prüfungsfenster"""
        def add_exam() -> None:
            """Neue Prüfung anlegen und zum Prüfungsmenu zurückkehren"""
            print('\nNeue Prüfung anlegen\n')
            exam_name = input('Prüfungsname: ')
            exam_notes = input('Notizen: ')

            new_exam = Exam(exam_name, exam_notes)

            # Aufgaben hinzugügen
            names_given = True if input('Aufgabennamen festlegen (j/n), sonst automatische Nummerierung') == 'j' \
                               else False

            numbering_scheme = ''
            if not names_given:
                numbering_schemes = [('1.1', 'task:number.subtask:number'),
                                     ('1a)', 'task:numbersubtask:letter)'),
                                     ('(1a)', '(task:numbersubtask:letter)')]
                print_numbered_list('Nummerierungschemata', [i[0] for i in numbering_schemes] + ['Eigenes Format'])
                try:
                    numbering_scheme = numbering_schemes[int(input('Geben Sie die Nummer einer Option ein: '))][1]
                except:
                    # hier gegebenenfalls formaterklärung hinzufügen
                    numbering_scheme = input('Geben Sie ihr Nummerierungsformat an: ')

            print('Geben Sie die erreichbare Punktzahl der Aufgabe ein;\n'
                  'Trennen Sie Aufgaben mit "," und Unteraufgaben mit " ";\n'
                  'Bei der Angabe von Aufgabennamen trennen Sie diese mit ":" von der nachfolgenden Punktzahl\n')
            tasks = input('Punktzahlen: ')
            new_exam.quick_add_tasks(tasks, names_given, numbering_scheme)

            exams.append(new_exam)

            exam_window()
        def edit_exam() -> None:
            ...

        def delete_exam() -> None:
            ...

        # Prüfungsfenster
        print_heading('Prüfungsverwaltung')
        print_numbered_list('Bestehende Prüfungen', [i.exam_name for i in exams])

        exam_window_menu_items = [('Prüfung hinzufügen', add_exam),
                                  ('Prüfung bearbeiten', edit_exam),
                                  ('Prüfung löschen', delete_exam),
                                  ('Zurück zum Hauptmenu', main_window)]
        print_menu(exam_window_menu_items)

    def result_window() -> None:
        ...

    def settings_window() -> None:
        ...

    def main_window() -> None:
        """Hauptmenu"""

        # Überschrift
        print_heading('Bewertungsrechner V1')

        # Menu
        main_window_menu_items = [('GUI starten', start_gui),
                                  ('Kursverwaltung', course_window),
                                  ('Prüfungsverwalung', exam_window),
                                  ('Ergebnissverwaltung', result_window),
                                  ('Einstellungen', settings_window)]
        print_menu(main_window_menu_items)


    main_window()

terminal_user_interface()