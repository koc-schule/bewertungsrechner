from . import *

IS_DEV = True
current_log_file_path = ""

def log(content: str) -> None:
    if not IS_DEV:
        return
    with open("logs/events.log", "a") as log:
        log.write(f"{content}\n")

def reset() -> None:
    if not IS_DEV:
        clear()
        return
    if not check():
        open("logs/events.log", "w").write("")
        return
    log = open("logs/events.log", "r").read()
    counter = sum(1 for f in Path("logs").iterdir() if f.is_file())
    log_old = open(f"logs/old_event_{counter}.log", "w").write(log)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_new = open("logs/events.log", "w").write(f"Event Log Nr. {counter + 1} at time {date}\n")

def check() -> bool:
    try:
        open("logs/events.log")
    except FileNotFoundError as exception:
        return False
    else:
        return True

def clear() -> None:
    if Path("logs").is_dir():
        [f.unlink() for f in Path('logs').iterdir() if f.is_file()]