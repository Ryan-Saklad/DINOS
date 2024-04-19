from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType
from utils.count_elements import count_elements
from utils.problem_type import ProblemType

class ElementCountConstraint(Constraint):
    # initialize from the parent class
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    def __init__(self, element_type: ElementType, element: str | None = None, min_count: int | None = None, max_count: int | None = None, exact_count: int | None = None, case_sensitive: bool = True) -> None:
        """
        Initializes the element count constraint with specific counts for validation.
        
        Args:
            element_type (ElementType): Specifies the type of elements to count (words, characters, sentences, paragraphs).
            element (str, optional): The specific element to count occurrences of. Defaults to None.
            min_count (int, optional): The minimum count of elements required. Defaults to None.
            max_count (int, optional): The maximum count of elements allowed. Defaults to None.
            exact_count (int, optional): The exact count of elements required. Defaults to None.
            case_sensitive (bool, optional): Whether the element counting should be case-sensitive. Defaults to True.
            
        Raises:
            ValueError: If the provided element type is not an instance of ElementType or if the count conditions are invalid.
        """
        if not isinstance(element_type, ElementType):
            raise ValueError("element_type must be an instance of ElementType")
        if exact_count and (min_count or max_count):
            raise ValueError("exact_count cannot be used with min_count or max_count")
        if min_count and max_count and min_count > max_count:
            raise ValueError("min_count cannot be greater than max_count")

        self.element_type: ElementType = element_type
        self.element: str | None = element
        self.min_count: int | None = min_count
        self.max_count: int | None = max_count
        self.exact_count: int | None = exact_count
        self.case_sensitive: bool = case_sensitive
        
        description_parts = [f"{element_type.name.lower()} count constraint:"]
        if element:
            description_parts.append(f"element '{element}'")
        if exact_count:
            description_parts.append(f"exactly {exact_count}")
        else:
            if min_count:
                description_parts.append(f"minimum {min_count}")
            if max_count:
                description_parts.append(f"maximum {max_count}")
        if not case_sensitive:
            description_parts.append("case-insensitive")
        description = " ".join(description_parts)
        super().__init__(description)
    
    def validate(self, response: str) -> bool:
        """
        Validates if the number of elements or occurrences of a specific element in the response meets the specified count constraints.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the number of elements or occurrences meets the constraints, False otherwise.
        """
        if self.element:
            element_count: int = count_elements(response, self.element_type, self.element, self.case_sensitive)
        else:
            element_count: int = count_elements(response, self.element_type, case_sensitive=self.case_sensitive)

        if self.exact_count and element_count != self.exact_count:
            if self.element:
                self.violations.append(f"The response contains {element_count} occurrences of '{self.element}', but exactly {self.exact_count} are required.")
            else:
                self.violations.append(f"The response contains {element_count} {self.element_type.name.lower()}, but exactly {self.exact_count} are required.")
            return False
        if self.min_count and element_count < self.min_count:
            if self.element:
                self.violations.append(f"The response contains {element_count} occurrences of '{self.element}', but a minimum of {self.min_count} are required.")
            else:
                self.violations.append(f"The count_elementsresponse contains {element_count} {self.element_type.name.lower()}, but a minimum of {self.min_count} are required.")
            return False
        if self.max_count and element_count > self.max_count:
            if self.element:
                self.violations.append(f"The response contains {element_count} occurrences of '{self.element}', but a maximum of {self.max_count} are allowed.")
            else:
                self.violations.append(f"The response contains {element_count} {self.element_type.name.lower()}, but a maximum of {self.max_count} are allowed.")
            return False
        return True
