from enum import Enum, auto


class OutputType(Enum):
    JSON = "JSON"
    YAML = "YAML"
    XML = "XML"
    WRAP = "WRAP"

    def __str__(self):
        return self.value