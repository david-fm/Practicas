import os
import pandas as pd
from tqdm import tqdm

def get_files():
    """Returns a list with the files in dominiopublico subfolder"""
    # Get directory of the current file
    cwd = os.path.dirname(__file__)+"/dominiopublico"
    # Get the list of files in the directory dominiopublico
    files = os.listdir(cwd)
    # Filter the list of files to only include the ones that end with ".csv"
    files = ['/'.join((cwd,file)) for file in files if file.endswith(".csv")]
    return files

def get_data():
    """Returns a pandas dataframe with the data from all the files in dominiopublico subfolder"""
    # Get the list of files
    files = get_files()
    # Create an empty list to store the dataframes
    dataframes = []
    # Loop through the files
    for file in tqdm(files):
        # Read the file as a dataframe and append it to the list
        dataframes.append(pd.read_csv(file, encoding='latin-1', sep=';', na_values=['']))
    # Concatenate all the dataframes in the list
    df = pd.concat(dataframes)
    df = df.astype('string')
    df = df.fillna('')
    return df

if __name__ == "__main__":
    # Get the data
    df = get_data()
    # Print the first 5 rows
    print(df.head(0))
    df.to_csv('data.csv', index=False, sep=';')