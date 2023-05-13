import re
def clean_text(text):
    """
    Delete all wierd characters from a text file
    :param file: File to clean
    """
    # Delete all the wierd characters
    text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,;:¿?¡! ]', '', text)
    # Delete all the patterns where there are a symbol that is not a letter or a number
    text = re.sub(r'[^a-zA-Z0-9 ][^a-zA-Z0-9 ]', ' ', text)
    # Change special characters from spanish language by its equivalent ona ASCII
    text = re.sub(r'[áÁ]', 'a', text)
    text = re.sub(r'[éÉ]', 'e', text)
    text = re.sub(r'[íÍ]', 'i', text)
    text = re.sub(r'[óÓ]', 'o', text)
    text = re.sub(r'[úÚ]', 'u', text)
    text = re.sub(r'[ñÑ]', 'n', text)
    # Save the text
    return text