from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType
from utils.count_elements import count_elements
from utils.problem_type import ProblemType

class FibonacciSequenceConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    """
    This class extends the Constraint class to check if the number of elements
    (words, characters, sentences, or paragraphs) in a given response text is a Fibonacci number.
    It leverages the count_elements function for more accurate counting of elements,
    and provides clear error messages for unsupported cases.
    """

    def __init__(self, element_type: ElementType) -> None:
        """
        Initializes the Fibonacci sequence constraint with a specific element type to count in the response.
        
        Args:
            element_type (ElementType): Specifies the type of elements to count (words, characters, sentences, paragraphs).
        
        Raises:
            ValueError: If the provided element type is not an instance of ElementType.
        """
        if not isinstance(element_type, ElementType):
            raise ValueError("element_type must be an instance of ElementType")

        self.element_type = element_type
        description = f"The number of {element_type.name.lower()} in the response must be a Fibonacci number."
        super().__init__(description)

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the number of elements in the response is a Fibonacci number.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the number of elements is a Fibonacci number, False otherwise.
        """
        element_count: int = count_elements(response, self.element_type)

        if element_count == 0:
            self.violations.append(f"The response contains no {self.element_type.name.lower()}, which does not satisfy the Fibonacci sequence constraint.")
            return False

        # Generating Fibonacci series up to the element count and checking if the count is in the series
        fib_series = [0, 1]
        while fib_series[-1] < element_count:
            fib_series.append(fib_series[-1] + fib_series[-2])
        if element_count in fib_series:
            return True
        else:
            self.violations.append(f"The number of {self.element_type.name.lower()} in the response ({element_count}) is not a Fibonacci number.")
            return False
