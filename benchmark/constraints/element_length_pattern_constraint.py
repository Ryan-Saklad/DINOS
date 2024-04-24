from benchmark.constraints.constraint import Constraint
from utils.count_elements import count_elements
from utils.element_type import ElementType
from utils.split_elements import split_elements
from utils.problem_type import ProblemType

class ElementLengthPatternConstraint(Constraint):
    problem_type = ProblemType.ELEMENT_CONSTRAINT
    def __init__(self, element_type: ElementType, scope_type: ElementType, increasing: bool, min_length_diff: int = 1) -> None:
        """
        Initializes the element length pattern constraint.
        
        Args:
            element_type (ElementType): The type of element to check length patterns for (words or sentences).
            scope_type (ElementType): The type of scope to apply the constraint to (sentences or paragraphs).
            increasing (bool): Whether the length pattern should be increasing (True) or decreasing (False).
            min_length_diff (int, optional): The minimum length difference between consecutive elements. Defaults to 1.
        
        Raises:
            ValueError: If the provided element type or scope type is invalid.
            ValueError: If min_length_diff is less than 1.
        """
        if element_type not in [ElementType.WORDS, ElementType.SENTENCES]:
            raise ValueError("element_type must be either ElementType.WORDS or ElementType.SENTENCES")
        if scope_type not in [ElementType.SENTENCES, ElementType.PARAGRAPHS]:
            raise ValueError("scope_type must be either ElementType.SENTENCES or ElementType.PARAGRAPHS")
        if min_length_diff < 1:
            raise ValueError("min_length_diff must be greater than or equal to 1")

        self.element_type: ElementType = element_type
        self.scope_type: ElementType = scope_type
        self.increasing: bool = increasing
        self.min_length_diff: int = min_length_diff

        pattern = "increasing" if increasing else "decreasing"
        description = f"The lengths of {element_type.name.lower()} within each {scope_type.name.lower()[:-1]} should be in {pattern} order"
        description += f" with a minimum length difference of {min_length_diff}"
        super().__init__(description)

    def validate(self, response: str, original_text: str = '') -> bool:
        """
        Validates if the response satisfies the element length pattern constraint, not allowing same length as valid.

        Args:
            response (str): The response text to validate.

        Returns:
            bool: True if the response satisfies the element length pattern constraint with no same lengths allowed, False otherwise.
        """
        scopes: list[str] = split_elements(response, self.scope_type)
        lengths: list[int] = [count_elements(scope, self.element_type) for scope in scopes]

        valid: bool = True

        if len(lengths) < 2:
            return True

        for i in range(1, len(lengths)):
            diff = lengths[i] - lengths[i-1]

            if (self.increasing and diff < self.min_length_diff) or (not self.increasing and -diff < self.min_length_diff):
                valid = False
                self.violations.append(f"The lengths of {self.element_type.name.lower()} within a {self.scope_type.name.lower()} are not strictly in {'increasing' if self.increasing else 'decreasing'} order with a minimum length difference of {self.min_length_diff}.")
                break

        return valid
