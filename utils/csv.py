"""
Modul für jegliche Operationen mit .csv-Dateien
"""

import output

def read_csv_base(path: str, reader: str) -> str | bool:
    """
    Basismethode für das Einlesen von .csv-Dateien.

    Args:
        path (str): Pfad der Datei
        reader (str): Funktion die auf die Datei angewandt werden soll (z.B. lambda)

    Returns:
        list[str] | bool: Inhalt der .csv-Datei oder False wenn Datei nicht existiert
    """
    try:
        content: list[str]
        with open(path) as file:
            content = reader(file)
        return content
    except FileNotFoundError as exception:
        output.log_exception(exception)
        return False

def read_csv_lines(path: str) -> list[str] | bool:
    """
    Liest eine .csv-Datei an einem gegebenem Pfad ein.

    Args:
        path (str): Pfad der Datei

    Returns:
        list[str] | bool: Inhalt der .csv-Datei als Liste aller Zeilen oder False wenn Datei nicht existiert
    """
    return read_csv_base(path, lambda file: file.readlines())

def read_csv(path: str) -> str | bool:
    """
    Liest eine .csv-Datei an einem gegebenem Pfad ein.

    Args:
        path (str): Pfad der Datei

    Returns:
        list[str] | bool: Inhalt der .csv-Datei oder False wenn Datei nicht existiert
    """
    return read_csv_base(path, lambda file: file.read())

def write_csv(path: str, content: str) -> None:
    """
    Schreibt eine neue .csv-Datei.
    Args:
        path (str): Pfad der Datei
        content (str): Inhalt der in die Datei geschrieben werden soll
    """
    with open(path, "w") as file:
        file.write(content)

def write_csv_append(path: str, content: str) -> None:
    """
    Schreibt eine bestehende .csv-Datei (fügt hinten hinzu).
    Args:
        path (str): Pfad der Datei
        content (str): Inhalt der in die Datei geschrieben werden soll
    """
    with open(path, "a") as file:
        file.write(content)