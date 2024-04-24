from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType
from utils.count_elements import count_elements
from utils.problem_type import ProblemType

class ElementFrequencyConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    def __init__(self, element_type: ElementType, element: str, min_frequency: float = None, max_frequency: float = None, case_sensitive: bool = True) -> None:
        """
        Initializes the element frequency constraint with specific frequency requirements for validation.
        
        Args:
            element_type (ElementType): The type of element to check frequency for (character, word, etc.).
            element (str): The specific element to check frequency for.
            min_frequency (float, optional): The minimum frequency percentage required. Defaults to None.
            max_frequency (float, optional): The maximum frequency percentage allowed. Defaults to None.
            case_sensitive (bool, optional): Whether the element comparison should be case-sensitive. Defaults to False.
            
        Raises:
            ValueError: If the provided element is empty or if the frequency conditions are invalid.
        """
        if not element:
            raise ValueError("element must not be empty")
        if not min_frequency and not max_frequency:
            raise ValueError("At least one of min_frequency or max_frequency must be specified")
        if min_frequency and max_frequency and min_frequency > max_frequency:
            raise ValueError("min_frequency cannot be greater than max_frequency")

        self.element_type: ElementType = element_type
        self.element: str = element
        self.min_frequency: float = min_frequency or 0.0
        self.max_frequency: float = max_frequency or 1.0
        self.case_sensitive: bool = case_sensitive

        description_parts = [f"{element_type.name.lower()} frequency constraint for '{element}':"]
        if min_frequency:
            description_parts.append(f"minimum {min_frequency}%")
        if max_frequency:
            description_parts.append(f"maximum {max_frequency}%")
        if not case_sensitive:
            description_parts.append("(case-insensitive)")
        description = " ".join(description_parts)
        super().__init__(description)

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the element frequency in the response meets the specified constraints.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the element frequency meets the constraints, False otherwise.
        """
        if not self.case_sensitive:
            response = response.lower()
            element = self.element.lower()
        else:
            element = self.element

        element_count: int = count_elements(response, self.element_type, element)
        total_elements: int = count_elements(response, self.element_type)
        frequency: float = (element_count / total_elements) if total_elements > 0 else 0.0

        if self.min_frequency and frequency < self.min_frequency:
            self.violations.append(f"The frequency of '{self.element}' in the response is {frequency:.2f}%, but a minimum of {self.min_frequency}% is required.")
            return False
        if self.max_frequency and frequency > self.max_frequency:
            self.violations.append(f"The frequency of '{self.element}' in the response is {frequency:.2f}%, but a maximum of {self.max_frequency}% is allowed.")
            return False
        return True
