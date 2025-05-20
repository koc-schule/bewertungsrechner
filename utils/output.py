"""
Methoden für die Ausgabe von generellen Informationen und Exceptions (effektiv als Alternazive für Konsolen)
"""

def log_exception(exception: str | Exception) -> None:
    """
    Gibt eine Fehlermeldung aus (aktuell nur print, vlt. später auch in ein Label auf der GUI)

    Args:
        exception (str | Exception): Die Fehlermeldung als String oder Exception selbst
    """
    if exception is str:
        print(exception)
        return
    if exception is Exception:
        print(str(exception))
        return