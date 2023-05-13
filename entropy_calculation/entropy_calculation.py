import os
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entropy import entropy
from clean_text import clean_text

def get_files():
    """Returns a list with the files in my directory
    :return: List of files"""
    # Get directory of the current file
    cwd = os.path.dirname(__file__)
    # Get the list of files in the directory dominiopublico
    files = os.listdir(cwd)
    # Filter the list of files to only include the ones that end with ".txt"
    files = ['/'.join((cwd,file)) for file in files if file.endswith(".txt")]
    return files

def get_clean_data(files):
    """Returns a list with the text of the files cleaned
    :param files: List of files to clean"""
    # Create an empty list for cleaned data
    data = []
    # Loop through the files
    for file in files:
        # Read the file as a dataframe and append it to the list
        with open(file, 'r') as f:
            data.append(clean_text(f.read()))
    return data

def get_entropy(files, data):
    """Creates a csv file with the entropy getting the 
    entropy with n being in the range [0-18] of the files
    :param files: List of files to calculate the entropy
    :param data: List of strings to calculate the entropy
    :return: list with the mean entropy per value of n"""
    # Create an empty list to store the dataframes
    dataframes = []
    # Loop through the files
    for i, text in enumerate(data):
        # Create a dictionary to store the entropy
        entropy_dict = {}
        # Loop through the range of n
        for n in range(18):
            # Calculate the entropy
            entropy_dict[n] = entropy(text, n)
        # Get the name of the file
        file = files[i].split('/')[-1]
        # Create a dataframe with the entropy
        df = pd.DataFrame(entropy_dict, index=[file])
        # Append the dataframe to the list
        dataframes.append(df)
    # Concatenate all the dataframes in the list
    df = pd.concat(dataframes)
    df.index.name = 'file'
    df.reset_index(inplace=True)

    # Save the dataframe as a csv file
    df.to_csv('entropy.csv', index=False, sep=';')

    # Calculate the mean entropy per value of n
    df = df.mean(axis=0)
    df = pd.DataFrame(df, columns=['entropy'])
    df.index.name = 'n'
    df.reset_index(inplace=True)
    # Save the dataframe as a csv file
    df.to_csv('mean_entropy.csv', index=False, sep=';')

    return df

if __name__ == "__main__":
    # Get the files
    files = get_files()
    # Get the data
    data = get_clean_data(files)
    # Get the entropy
    df = get_entropy(files, data)
    # Print the first 5 rows
    print(df)


