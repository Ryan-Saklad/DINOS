import re

from utils.element_type import ElementType

def count_elements(response: str, element_type: ElementType) -> int:
    """
    Counts the elements in the response based on the specified element type.
    
    Args:
        response (str): The response text to count elements in.
        element_type (ElementType): The type of elements to count.
        
    Returns:
        int: The count of elements in the response.
        
    Raises:
        TypeError: If the response is not a string.
        ValueError: If an unsupported element type is specified.
    """
    if not isinstance(response, str):
        raise TypeError("Response must be a string")

    # Counting words using regular expressions to match alphanumeric characters
    if element_type == ElementType.WORDS:
        words = re.findall(r'\w+', response)
        return len(words)
    # Counting all characters including spaces and punctuation
    elif element_type == ElementType.CHARACTERS:
        return len(response)
    # Using regular expressions to split text into sentences based on punctuation followed by space or end of string
    elif element_type == ElementType.SENTENCES:
        sentences = re.split(r'[.!?](?:\s+|$)', response)
        # Filtering out empty strings to get the accurate sentence count
        return len([sentence for sentence in sentences if sentence.strip()])
    # Splitting text into paragraphs based on two newline characters, considering non-empty paragraphs only
    elif element_type == ElementType.PARAGRAPHS:
        paragraphs = re.split(r'\n\s*\n', response)
        return len([para for para in paragraphs if para.strip()])
    else:
        # Raising an error for unsupported element types
        raise ValueError(f"Unsupported element type: {element_type}")
