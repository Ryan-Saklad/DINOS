from abc import ABC

class BenchmarkTask(ABC):
    def __init__(self):
        pass

    @staticmethod
    def strip_boilerplate(response: str) -> str:
        """Takes the raw model response and strips the boilerplate
        text generally found in the first line of text."""
        if not isinstance(response, str):
            return response

        fmt_response = response.lstrip()
        lines = fmt_response.split('\n')
        if len(lines) < 2:
            return ''
        fmt_response = '\n'.join(lines[1:])
        return fmt_response.lstrip()  # don't keep any leading whitespace
