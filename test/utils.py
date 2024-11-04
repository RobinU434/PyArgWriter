from typing import Iterable, Type


def stderr_is_relevant(stderr: str):
    if "Traceback" in stderr:
        return True
    for line in stderr.split("\n"):
        msg_entity = line.split(":")[0]
        if msg_entity.lower() in ["error", "fatal", "critical"]:
            print("detected: ", msg_entity)
            return True
    return False