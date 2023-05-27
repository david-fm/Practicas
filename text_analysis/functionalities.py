# Give functionalities to process metadata for the text analysis

def get_name(authors):
    # Return the name of the author
    # Example "Elizondo, Francisco Antonio de  // Mar\u00edn, Pedro , fl. 1763?-1790 -imp.  //",
    authors = authors.split("//")
    author = authors[0]
    author = author.split(",")
    if 'fl.' in author[-1] or 's.' in author[-1] or '-' in author[-1]:
        author = author[:-1]
    author_name = author[-1].strip()
    author_name = author_name.split(" ")[0]
    return author_name

def gender(name) -> str:
    '''
        Get through the api the gender of the person
        :param name: name of the person
        :return: None if the api limit gotten or the gender of the person
        '''
    # return if the name is male or not
    import requests
    try:
        # Get the first name
        response = requests.get("https://api.genderize.io/?name=" + name + "&country_id=ES")
        response_json = response.json()
    
        return response_json['gender']
    except:
        return None

def counting_males(csv):
    # Count how many males there are in the csv file
    # Having in mind that it is in the gender column
    import pandas
    dataframe = pandas.read_csv(csv)
    dataframe = dataframe.dropna()
    males = dataframe[dataframe.gender == 'male']
    women = dataframe[dataframe.gender != 'male']
    print(males.shape[0])
    print(dataframe.shape[0])
    print(women)

if __name__ == "__main__":
    # Test get_name function by saving a csv file with the name of all the authers 
    # in books/metadata.json
    import json
    import pandas
    with open('/Users/davidflorezmazuera/Library/CloudStorage/GoogleDrive-270191@student.pwr.edu.pl/Mi unidad/Spanish_V2/metadata.json') as f:
        data = json.load(f)
    # get the name of the authors and the corpus identifier
    # the corpues identifier will be given as a list of the books 
    # obtained from the union of the book_id and number_of_volumes

    obtained_data = {}
    for book in data:
        obtained_data[book['book_id']] = (get_name(book['author']), book['number_of_volumes'])
    # get the gender of the authors and add it to the dataframe

    for_data_frame = {}
    for key in obtained_data:
        author = obtained_data[key][0]
        if author != '' and len(author)>2: 
            # if the author is not empty and its name is full (ex. is not 'M.') which is ambiguous
            author_gender = gender(author)
            if not author_gender:
                # if the api limit is reached
                break
            for i in range(obtained_data[key][1]):
                idb = f'{key}_{i}'
                for_data_frame[idb] = (author, author_gender)

    # Create the dataframe from the dictionary
    dataframe = pandas.DataFrame()
    dataframe['book_id'] = [key for key in for_data_frame]
    dataframe['author'] = [for_data_frame[key][0] for key in for_data_frame]
    dataframe['gender'] = [for_data_frame[key][1] for key in for_data_frame]
    dataframe.to_csv("authors.csv")

'''
counting_males("authors.csv")'''