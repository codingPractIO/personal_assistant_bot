from enum import StrEnum, auto


class Events(StrEnum):
    message_text = auto()

    activate_node = auto()
    deactivate_node = auto()
