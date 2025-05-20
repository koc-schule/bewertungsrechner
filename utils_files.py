"""
Modul für jegliche Operationen mit Dateien.
"""

import utils_general

def read_csv_base(path: str, reader: str):
    """
    Liest eine .csv-Datei an einem gegebenem Pfad ein.

    Args:
        path (str): Pfad der Datei

    Returns:
        list[str] | bool: Inhalt der .csv-Datei oder False wenn Datei nicht existiert
    """
    try:
        content: list[str]
        with open(path) as file:
            content = reader(file)
        return content
    except FileNotFoundError as exception:
        utils_general.log_exception(exception)
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
    _summary_

    Args:
        path (str): _description_
        content (str): _description_
    """
    with open(path, "w") as file:
        file.write(content)

def write_csv_append(path: str, content: str) -> None:
    """
    _summary_

    Args:
        path (str): _description_
        content (str): _description_
    """
    with open(path, "a") as file:
        file.write(content)


if __name__ == "__main__":
    PATH = "test_files.csv"
    print(read_csv(PATH))
    print(read_csv_lines(PATH))