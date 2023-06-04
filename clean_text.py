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
    # Delete heading and footers
    text = re.sub(r'Biblioteca Nacional de Espana', '', text)
    # Save the text
    return text


def clean_file(directory, file):
    """
    Clean a file
    :param directory: Directory where the file is
    :param file: File to clean
    """
    import os
    # Read the file
    with open(os.path.join(directory, file), 'r', encoding='latin-1') as f:
        text = f.read()
    # Clean the text
    text = clean_text(text)
    # Save the text
    with open(os.path.join(directory, file), 'w', encoding='latin-1') as f:
        f.write(text)

def clean_directory_files_parallel(directory):
    """
    Clean all the files in a directory
    :param directory: Directory to clean
    """
    import os
    from joblib import Parallel, delayed
    # Get all the files in the directory
    files = os.listdir(directory)
    # Clean all the files
    Parallel(n_jobs=-1)(delayed(clean_file)(directory, file) for file in files)

def count_words(directory, file):
    """
    Count the number of words in a file
    :param directory: Directory where the file is
    :param file: File to count the words
    :return: Number of words in the file
    """
    import os
    # Read the file
    with open(os.path.join(directory, file), 'r', encoding='latin-1') as f:
        text = f.read()
    # Count the number of words
    num_words = len(text.split())
    # Save the number of words
    return num_words

def update_num_words_parallel(directory, metadata):
    """
    Update the number of words of the metadata
    :param metadata: Metadata to update
    """
    import os
    import json
    from joblib import Parallel, delayed
    # Get all the files in the directory
    files = os.listdir(directory)
    # count the number of words in each file
    num_words = Parallel(n_jobs=-1)(delayed(count_words)(directory, file) for file in files)
    # Update the metadata
    metadata = os.path.join(directory, metadata)
    with open(metadata, 'r', encoding='latin-1') as f:
        data = json.load(f)
    data['num_words'] = num_words # TODO
    with open(metadata, 'w', encoding='latin-1') as f:
        json.dump(data, f, indent=4)
if __name__ == '__main__':
    # /Users/davidflorezmazuera/Library/CloudStorage/GoogleDrive-270191@student.pwr.edu.pl/Mi unidad/Spanish_tests
    directory = input('Introduce the directory where the files are: ')
    clean_directory_files_parallel(directory)