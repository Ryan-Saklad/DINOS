import re  # Importing regular expressions module for improved element counting

from benchmark.constraints.constraint import Constraint
from utils.element_type import ElementType

class FibonacciSequenceConstraint(Constraint):
    """
    This class extends the Constraint class to check if the number of elements
    (words, characters, sentences, or paragraphs) in a given response text is a Fibonacci number.
    It uses regular expressions for more accurate counting, especially for words and sentences,
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

    def count_elements(self, response: str) -> int:
        """
        Counts the elements in the response based on the specified element type.
        
        Args:
            response (str): The response text to count elements in.
        
        Returns:
            int: The count of elements in the response.
        
        Raises:
            TypeError: If the response is not a string.
        """
        if not isinstance(response, str):
            raise TypeError("Response must be a string")

        if self.element_type == ElementType.WORDS:
            # Using regular expressions to count words, considering alphanumeric characters as part of words
            words = re.findall(r'\w+', response)
            return len(words)
        elif self.element_type == ElementType.CHARACTERS:
            # Counting all characters, including spaces and punctuation
            return len(response)
        elif self.element_type == ElementType.SENTENCES:
            # Using regular expressions to split text into sentences based on punctuation followed by space or end of string
            sentences = re.split(r'[.!?](?:\s+|$)', response)
            # Filtering out empty strings to get the accurate sentence count
            return len([sentence for sentence in sentences if sentence.strip()])
        elif self.element_type == ElementType.PARAGRAPHS:
            # Splitting text into paragraphs based on two newline characters, considering non-empty paragraphs only
            paragraphs = re.split(r'\n\s*\n', response)
            return len([para for para in paragraphs if para.strip()])
        else:
            # Raising an error for unsupported element types
            raise ValueError(f"Unsupported element type: {self.element_type}")

    def validate(self, response: str) -> bool:
        """
        Validates if the number of elements in the response is a Fibonacci number.
        
        Args:
            response (str): The response text to validate.
        
        Returns:
            bool: True if the number of elements is a Fibonacci number, False otherwise.
        """
        element_count = self.count_elements(response)
        if element_count == 0:
            return False

        # Generating Fibonacci series up to the element count and checking if the count is in the series
        fib_series = [0, 1]
        while fib_series[-1] < element_count:
            fib_series.append(fib_series[-1] + fib_series[-2])
        return element_count in fib_series
