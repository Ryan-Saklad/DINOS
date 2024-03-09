import re

from utils.element_type import ElementType

def count_elements(response: str, element_type: ElementType, element: str | None = None, case_sensitive: bool = True) -> int:
    """
    Counts the elements in the response based on the specified element type.
    
    Args:
        response (str): The response text to count elements in.
        element_type (ElementType): The type of elements to count.
        element (str | None, optional): The specific element to count. Defaults to None.
        case_sensitive (bool, optional): Whether the element comparison should be case-sensitive. Defaults to True.
        
    Returns:
        int: The count of elements in the response.
        
    Raises:
        TypeError: If the response is not a string.
        ValueError: If an unsupported element type is specified.
    """
    if not isinstance(response, str):
        raise TypeError("Response must be a string")

    if not case_sensitive:
        response = response.lower()
        if element:
            element = element.lower()

    match element_type:
        case ElementType.WORDS:
            words = re.findall(r'\w+', response)
            return len([word for word in words if word == element]) if element else len(words)
        case ElementType.CHARACTERS:
            return response.count(element) if element else len(response)
        case ElementType.SENTENCES:
            sentences = re.split(r'[.!?](?:\s+|$)', response)
            sentences = [sentence for sentence in sentences if sentence.strip()]
            return len([sentence for sentence in sentences if element in sentence]) if element else len(sentences)
        case ElementType.PARAGRAPHS:
            paragraphs = re.split(r'\n\s*\n', response)
            paragraphs = [para for para in paragraphs if para.strip()]
            return len([para for para in paragraphs if element in para]) if element else len(paragraphs)
        case _:
            raise ValueError(f"Unsupported element type: {element_type}")
