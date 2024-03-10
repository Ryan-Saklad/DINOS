import re
from utils.element_type import ElementType

def split_elements(text: str, element_type: ElementType) -> list[str]:
    """
    Splits the text into elements based on the specified element type.
    
    Args:
        text (str): The text to split into elements.
        element_type (ElementType): The type of elements to split the text into.
        
    Returns:
        list[str]: The list of elements in the text.
        
    Raises:
        TypeError: If the text is not a string.
        ValueError: If an unsupported element type is specified.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string")

    match element_type:
        case ElementType.WORDS:
            return re.findall(r'\b\w+\b', text)
        case ElementType.CHARACTERS:
            return list(text)
        case ElementType.SENTENCES:
            return re.split(r'(?<=[.!?])\s+', text)
        case ElementType.PARAGRAPHS:
            return re.split(r'\n\s*\n', text)
        case _:
            raise ValueError(f"Unsupported element type: {element_type}")
