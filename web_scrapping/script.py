'''
This script is used to create the books from the data through the API
and save them 
https://datosabiertos.bne.es/dataset/biblioteca-digital-documentos-en-dominio-publico/
'''

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import api
from save_object import save_object, load_object
import regex as re
import json
from tqdm import tqdm
import requests
from clean_text import clean_text
from entropy import entropy

class Book:
    def __init__(self, title, author, date, origin_country,language, subject, genre, digital_version, ocr):
        self.title = title
        self.author = author # Peron who is said to be the author of a book
        self.date = date
        self.origin_country = origin_country
        self.language = language
        self.subject = subject
        self.genre = genre
        self.digital_version = digital_version
        self.ocr = ocr
        self.words = 0
        self.book_id = None
        self.number_of_volumes = None
        self.entropy = None

    def __str__(self) -> str:
        return f"{self.title} - {self.author} - {self.date} - {self.origin_country} - {self.language} - {self.subject} - {self.genre} - {self.digital_version} - {self.ocr}"


    @classmethod
    def from_json(self, title, author, date, origin_country,language, subject, genre, digital_version, ocr, words, book_id, number_of_volumes, entropy):
        
        book = self(title, author, date, origin_country,language, subject, genre, digital_version, ocr)
        book.words = words
        book.book_id = book_id
        book.number_of_volumes = number_of_volumes
        book.entropy = entropy
        return book
        

class Library:
    def __init__(self, books: list):
        self.books = books

    def __str__(self) -> str:
        return f"{self.books}"
    
    def __getitem__(self, index) -> Book:
        return self.books[index]

    @classmethod
    def from_api(self) -> "Library":
        """Load books from api"""
        books = []
        for index, row in tqdm(api.get_data().iterrows()):
            if row['Tipo de documento'] == 'Libro' or row['Tipo de documento'] == 'Manuscrito':
                books.append(
                    Book(
                    row['Título'], 
                    row['Autor Personas'], 
                    row['Fecha de publicación'], 
                    row['País de publicación'], 
                    row['Lengua de publicación'], 
                    row['Tema'], 
                    row['Género/Forma'], 
                    row['version_digital'], 
                    row['texto_OCR']))
            
        return self(books)
    @classmethod
    def from_pickle(self) -> "Library":
        """Load books from pickle format"""
        self.books = load_object("books.pkl")
        return self(self.books)

    @classmethod
    def from_books_path(self, path: str) -> "Library":
        '''Load books from the path that contains the books in .txt format and the metadata.json file'''
        books = []
        with open(f'{path}/metadata.json') as json_file:
            data = json.load(json_file)
            for book in tqdm(data):
                books.append(Book.from_json(book['title'], book['author'], book['date'], book['origin_country'], book['language'], book['subject'], book['genre'], book['digital_version'], book['ocr'], book['words'], book['book_id'], book['number_of_volumes'], book['entropy']))
        return self(books)

    def save_books(self):
        """Save books in pickle format"""
        save_object(self.books, "books.pkl")
    
    def save_ocr_books(self, directory='books', number_of_books=1000):
        """Save books that have a txt version in OCR
        Args:
            directory (str, optional): Directory where the books will be saved. Defaults to 'books'.
            number_of_books (int, optional): Number of books to save, if it is -1 it will download all dataset. Defaults to 1000.
        """
        if directory == '':
            directory = 'books'
        if not os.path.exists(directory):
            print("The folder does not exist")
            print("Creating the folder")
            os.makedirs(directory)
        directory = directory if directory[-1] != '/' and directory[-1] != '\\' else directory[:-1]
        counter = 0
        valid_books = []
        for book in tqdm(self.books):
            if book.ocr:
                counter = self.getting_and_writing_books(book, counter, valid_books, directory)
                if counter == number_of_books or number_of_books == -1:
                    break
        with open(f'{directory}/metadata.json', 'w') as fp:
            json.dump([book.__dict__ for book in tqdm(valid_books)], fp, indent=4)
                
    def getting_and_writing_books(self, book, counter, valid_books, directory):
        """"""
        book_urls = book.ocr.strip('* ').split(' ** ')
        book.number_of_volumes = len(book_urls)
        valid = False
        for i, url in enumerate(book_urls):
            response = requests.get(url)

            reg = re.compile(r'[^ \n]') # Check if the book is not empty
            if response.status_code == 200 and re.search(reg, response.text) :
                text = response.text
                # Clean the book
                text = clean_text(text)
                # Get the entropy on n = [1-18]
                book.entropy = [entropy(text, n) for n in range(1, 19)]

                # Save the book
                with open(f'{directory}/{counter}_{i}.txt', 'w') as fp:
                    fp.write(text)
                book.words = len(re.findall(r'\w+', text))
                book.book_id = counter
                valid = True
            
        if valid: 
            valid_books.append(book)
            counter += 1
        return counter


            


# Main to load the books and print the first one
'''
if __name__ == "__main__":
    Books = Library.from_pickle()
    for book in Books:
        print('Persons author:',book.author, 'Persons entity:', book.entity_author, 'Date:', book.date)
'''

# Main to create the books
if __name__ == "__main__":
    # Transform the data into a list of books
    Books = Library.from_pickle()
    # Save the books in pickle format
    Books.save_ocr_books()
