from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType
from utils.count_elements import count_elements

class ElementCountConstraint(Constraint):
    def __init__(self, element_type: ElementType, min_count: int = None, max_count: int = None, exact_count: int = None) -> None:
        """
        Initializes the element count constraint with specific counts for validation.
        
        Args:
            element_type (ElementType): Specifies the type of elements to count (words, characters, sentences, paragraphs).
            min_count (int, optional): The minimum count of elements required. Defaults to None.
            max_count (int, optional): The maximum count of elements allowed. Defaults to None.
            exact_count (int, optional): The exact count of elements required. Defaults to None.
            
        Raises:
            ValueError: If the provided element type is not an instance of ElementType or if the count conditions are invalid.
        """
        if not isinstance(element_type, ElementType):
            raise ValueError("element_type must be an instance of ElementType")
        if exact_count is not None and (min_count is not None or max_count is not None):
            raise ValueError("exact_count cannot be used with min_count or max_count")
        if min_count is not None and max_count is not None and min_count > max_count:
            raise ValueError("min_count cannot be greater than max_count")

        self.element_type = element_type
        self.min_count = min_count
        self.max_count = max_count
        self.exact_count = exact_count
        description_parts = [f"{element_type.name.lower()} count constraint:"]
        if exact_count is not None:
            description_parts.append(f"exactly {exact_count}")
        else:
            if min_count is not None:
                description_parts.append(f"minimum {min_count}")
            if max_count is not None:
                description_parts.append(f"maximum {max_count}")
        description = " ".join(description_parts)
        super().__init__(description)

    def validate(self, response: str) -> bool:
        """
        Validates if the number of elements in the response meets the specified count constraints.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the number of elements meets the constraints, False otherwise.
        """
        element_count: int = count_elements(response, self.element_type)

        if self.exact_count is not None and element_count != self.exact_count:
            self.violations.append(f"The response contains {element_count} {self.element_type.name.lower()}, but exactly {self.exact_count} are required.")
            return False
        if self.min_count is not None and element_count < self.min_count:
            self.violations.append(f"The response contains {element_count} {self.element_type.name.lower()}, but a minimum of {self.min_count} are required.")
            return False
        if self.max_count is not None and element_count > self.max_count:
            self.violations.append(f"The response contains {element_count} {self.element_type.name.lower()}, but a maximum of {self.max_count} are allowed.")
            return False
        return True
