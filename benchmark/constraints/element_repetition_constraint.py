from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType
from utils.split_elements import split_elements
from utils.problem_type import ProblemType

class ElementRepetitionConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    def __init__(self, element_type: ElementType, element: str, min_repetitions: int = None, max_repetitions: int = None, scope_type: ElementType = ElementType.PARAGRAPHS, case_sensitive: bool = True) -> None:
        """
        Initializes the element repetition constraint.
        
        Args:
            element_type (ElementType): The type of element to restrict repetitions for (characters or words).
            element (str): The specific element (character or word) to restrict repetitions for.
            min_repetitions (int, optional): The minimum number of times the element should be repeated within a scope. Defaults to None.
            max_repetitions (int, optional): The maximum number of times the element can be repeated within a scope. Defaults to None.
            scope_type (ElementType, optional): The type of scope to apply the constraint to (sentences or paragraphs). Defaults to ElementType.PARAGRAPHS.
            case_sensitive (bool, optional): Whether the element comparison should be case-sensitive. Defaults to True.
        
        Raises:
            ValueError: If the provided element type is not characters or words.
            ValueError: If both min_repetitions and max_repetitions are None.
            ValueError: If min_repetitions is greater than max_repetitions.
        """
        if element_type not in [ElementType.CHARACTERS, ElementType.WORDS]:
            raise ValueError("element_type must be either ElementType.CHARACTERS or ElementType.WORDS")
        if min_repetitions is None and max_repetitions is None:
            raise ValueError("At least one of min_repetitions or max_repetitions must be specified")
        if min_repetitions is not None and max_repetitions is not None and min_repetitions > max_repetitions:
            raise ValueError("min_repetitions cannot be greater than max_repetitions")

        self.element_type: ElementType = element_type
        self.element: str = element
        self.min_repetitions: int = min_repetitions
        self.max_repetitions: int = max_repetitions
        self.scope_type: ElementType = scope_type
        self.case_sensitive: bool = case_sensitive

        description = f"The {element_type.name.lower()[:-1]} '{element}' should"
        if min_repetitions is not None and max_repetitions is not None:
            description += f" be repeated between {min_repetitions} and {max_repetitions} times"
        elif min_repetitions is not None:
            description += f" be repeated at least {min_repetitions} time(s)"
        else:
            description += f" not be repeated more than {max_repetitions} time(s)"
        description += f" within each {scope_type.name.lower()[:-1]}"
        description += " (case-sensitive)" if case_sensitive else " (case-insensitive)"
        super().__init__(description)

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the response satisfies the element repetition constraint.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the response satisfies the element repetition constraint, False otherwise.
        """
        fmt_response = self.strip_boilerplate(response)
        scopes: list[str] = split_elements(fmt_response, self.scope_type)

        for scope in scopes:
            if self.element_type == ElementType.WORDS:
                elements = split_elements(scope, ElementType.WORDS)
            else:
                elements = split_elements(scope, ElementType.CHARACTERS)

            if not self.case_sensitive:
                elements = [e.lower() for e in elements]
                element = self.element.lower()
            else:
                element = self.element

            element_count: int = elements.count(element)

            if self.min_repetitions is not None and element_count < self.min_repetitions:
                self.violations.append(f"The {self.element_type.name.lower()[:-1]} '{element}' is repeated less than {self.min_repetitions} time(s) within a {self.scope_type.name.lower()[:-1]}.")
                return False
            if self.max_repetitions is not None and element_count > self.max_repetitions:
                self.violations.append(f"The {self.element_type.name.lower()[:-1]} '{element}' is repeated more than {self.max_repetitions} time(s) within a {self.scope_type.name.lower()[:-1]}.")
                return False

        return True