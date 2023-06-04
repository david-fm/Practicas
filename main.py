'''
    This is the main file of the project.
    It contains the control functions of the different parts of the project.
'''
from web_scrapping.script import Library
import os
import json
from metadata_cleaning import clean_authors

def main():
    '''
        This function is used to create the books from the data through the API
        and save them 
        https://datosabiertos.bne.es/dataset/biblioteca-digital-documentos-en-dominio-publico/
    '''
    if not os.path.exists('books.pkl'):
        print("Creating books objects and saving them")
        library = Library.from_api()
        library.save_books()
    else:
        print("Loading library")
        library = Library.from_pickle()
    flag = input("Do you want to download the books into a folder? If not, the program will stop here. (y/n)")
    if flag == 'y':
        route = input("Please, specify the route where you want to save the books: ")
        print("Downloading the books into the folder specified")
        number_of_books = int(input("How many books do you want to download? Write -1 if you want to download all the books: "))
        library.save_ocr_books(route, number_of_books)
        print("Cleaning the metadata of the books")
        route = 'books' if route == '' else route
        metadata = route + '/metadata.json'
        with open(metadata, encoding = 'latin-1') as f:
            data = json.load(f)
        data = clean_authors(data)
        with open(metadata, 'w', encoding = 'latin-1') as f:
            json.dump(data, f, indent = 4)

if __name__ == "__main__":
    main()

