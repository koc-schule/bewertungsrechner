from . import *

IS_DEV = False
CLEAR_OLD_LOGS = True
current_log_file_path = ""

def log(content: str) -> None:
    """
    Schreibt in eine .log Datei

    Args:
        content (str): Content
    """
    if not IS_DEV:
        return
    with open("logs/events.log", "a") as log:
        log.write(f"{content}\n")

def reset() -> None:
    """
    Erstellt neue logs
    """
    if CLEAR_OLD_LOGS:
        clear_logs()
    if not IS_DEV:
        return
    
    if not exists_directory_and_log():
        open("logs/events.log", "w").write("")
        return
    
    log = open("logs/events.log", "r").read()
    counter = sum(1 for f in Path("logs").iterdir() if f.is_file())
    log_old = open(f"logs/old_event_{counter}.log", "w").write(log)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_new = open("logs/events.log", "w").write(f"Event Log Nr. {counter + 1} at time {date}\n")

def exists_directory_and_log() -> bool:
    """
    Prüft ob /logs Ordner und logs/events.log existiert. Legt /logs an, wenn nicht existiert

    Returns:
        bool: False wenn events.log nicht existiert, True wenn existiert
    """
    if not Path("logs").is_dir():
        os.mkdir("logs")
        return False
    elif not Path("logs/events.log").is_file():
        return False
    else:
        return True

def clear_logs() -> None:
    """
    Löscht alle bestehenden Dateien im /log Ordner
    """
    if Path("logs").is_dir():
        [f.unlink() for f in Path('logs').iterdir() if f.is_file()]
        [f.unlink() for f in Path('logs').iterdir() if f.is_file()]

# Führt bei import aus   
reset()