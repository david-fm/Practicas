'''
    This is the main file of the project.
    It contains the control functions of the different parts of the project.
'''
from web_scrapping.script import Library, Book
import os

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
        route = route if route[-1] != '/' and route[-1] != '\\' else route[:-1]
        print("Downloading the books into the folder specified")
        number_of_books = int(input("How many books do you want to download? Write -1 if you want to download all the books: "))
        library.save_ocr_books(route, number_of_books)


if __name__ == "__main__":
    main()

