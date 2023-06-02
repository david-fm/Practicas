# Clening the metadata based on the undersired patterns spcified on the file clean_authors.txt
# This patterns where optain by manual extraction from the metadata file

import re

def clean_authors(books):
    # Match centuries and remove them, they are represented as .S XVI
    date = re.compile('[0-9][0-9][0-9][0-9]([^,]*[0-9]+)*')
    wrongly_writen_date = re.compile('-[0-9]+')
    # Remove parts that match with the next pattern [0-9][0-9][0-9][0-9]([^,]*[0-9]+)*
    century = re.compile('[sS]. [IVXLC]+')
    name = re.compile('^\s*[^\W\d_]{3,}', re.UNICODE)
    info_between_brackets = re.compile('\(.*\)')
    extra_info = re.compile('-.*')
    # Cleaning the authors
    for book in books:
        authors = book['author']
        authors = authors.split("//")

        for author in authors:
            authors_parts = author.split(",")
            
            for part in authors_parts:
                
                new_part = part
                if date.search(part):
                    
                    # Remove if at the begining there aren't more than 2 letters
                    if not name.search(part):
                        new_part = ''
                    # if match remove only the part that matches mantaining the position of the part
                    else:
                        new_part = date.sub('', part)
                elif wrongly_writen_date.search(part):
                    new_part = ''
                elif century.search(part):
                    new_part = ''
                
                elif info_between_brackets.search(part):
                    new_part = info_between_brackets.sub('', part)
                
                new_part = extra_info.sub('', new_part)
                new_part = new_part.lstrip()
                authors_parts[authors_parts.index(part)] = new_part

            authors_parts = [part for part in authors_parts if name.search(part)]
            authors[authors.index(author)] = ",".join(authors_parts)
        book['author'] = "//".join(authors)

    
    return books
                

def test_regex(text):
    # Test the regular expressions against a text
    date = re.compile('[0-9][0-9][0-9][0-9]([^,]*[0-9]+)*')
    wrongly_writen_date = re.compile('-[0-9]+')
    # Remove parts that match with the next pattern [0-9][0-9][0-9][0-9]([^,]*[0-9]+)*
    century = re.compile('[sS]. [IVXLC]+')
    name = re.compile('^\s*[^\W\d_]{3,}', re.UNICODE)
    info_between_brackets = re.compile('\(.*\)')
    extra_info = re.compile('-.*')
    with open(text, 'r') as input_file, open('regex_result.txt', 'w') as output_file:
        for line in input_file:
            if date.search(line):
                            
                # Remove if at the begining there aren't more than 2 letters
                if not name.search(line):
                    line = ''
                # if match remove only the part that matches mantaining the position of the part
                else:
                    line = date.sub('', line)

            elif wrongly_writen_date.search(line):
                line = ''
            elif info_between_brackets.search(line):
                line = info_between_brackets.sub('', line)
            
            elif century.search(line):
                # remove the line
                line = ''
            elif name.search(line):
                line = extra_info.sub('', line)
                line = line.lstrip()
            output_file.write(line)


if __name__ == '__main__':
    if (input('Do you want to test the regex? (y/n)') == 'y'):
        test_regex(input('Enter the path to the file to test: '))
    else:
        import json
        # /Users/davidflorezmazuera/Library/CloudStorage/GoogleDrive-270191@student.pwr.edu.pl/Mi unidad/Spanish_V2/metadata.json
        metadata = input('Enter the path to the metadata file: ')
        with open(metadata, encoding = 'latin-1') as f:
            data = json.load(f)
        data = clean_authors(data)
        import os
        dirname = os.path.dirname(metadata)
        basename = os.path.basename(metadata)
        new_metadata = basename.split('.')[0] + '_cleaned.json'
        metadata = os.path.join(dirname, new_metadata)
        with open(metadata, 'w') as f:
            json.dump(data, f, indent=4)
