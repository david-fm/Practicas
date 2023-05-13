import api
from save_object import save_object, load_object
import regex as re
import json
from tqdm import tqdm
import requests
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    def clean_book(self):
        """Clean the book data"""
        # TODO There could be many volumes of the same book
        # TODO There could be books that are not understandable due to the OCR
        # TODO There could be books that are not in Spanish
        # Delete the string , fl. .*// from the author column
        self.author = re.sub(r', [\- 0-9]*//', '//', self.author)


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

    def clean_library(self):
        """Clean the library data by:
        - Deleting the books that are not in Spanish
        - Deleting the books that are not in the same format
        """
    def save_books(self):
        """Save books in pickle format"""
        save_object(self.books, "books.pkl")
    
    def save_ocr_books(self):
        """Save books that have a txt version in OCR"""
        counter = 0
        valid_books = []
        for book in tqdm(self.books):
            if book.ocr:
                counter = self.getting_and_writing_books(book, counter, valid_books)
                if counter == 1000:
                    break
        with open('books/metadata.json', 'w') as fp:
            json.dump([book.__dict__ for book in tqdm(valid_books)], fp, indent=4)
                
    def getting_and_writing_books(self, book, counter, valid_books):
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
                with open(f'books/{counter}_{i}.txt', 'w') as fp:
                    fp.write(text)
                book.words = len(re.findall(r'\w+', text))
                book.book_id = counter
                valid = True
            
        if valid: 
            valid_books.append(book)
            counter += 1
        return counter

    
    def upload_to_one_drive(self):
        """Upload the books to one drive"""
        pass

            


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
