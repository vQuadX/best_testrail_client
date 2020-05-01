import enum


class FieldType(enum.Enum):
    STRING = 1
    INTEGER = 2
    TEXT = 3
    URL = 4
    CHECKBOX = 5
    DROPDOWN = 6
    USER = 7
    DATE = 8
    MILESTONE = 9
    STEP_RESULTS = 11
    MULTI_SELECT = 12
