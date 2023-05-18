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

def gender(name):
    # return if the name is male or not
    import requests
    # Get the first name
    response = requests.get("https://api.genderize.io/?name=" + name + "&country_id=ES")
    response_json = response.json()
    return response_json['gender']

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

'''if __name__ == "__main__":
    # Test get_name function by saving a csv file with the name of all the authers 
    # in books/metadata.json
    import json
    import pandas
    with open('books/metadata.json') as f:
        data = json.load(f)
    authors = []
    for book in data:
        authors.append(get_name(book['author']))
    # get the gender of the authors and add it to the dataframe
    genders = []
    used_authors = []
    for author in authors:
        if author != '' and len(author)>2: 
            # if the author is not empty and its name is full (ex. is not 'M.') which is ambiguous
            genders.append(gender(author))
            used_authors.append(author)
    dataframe = pandas.DataFrame()
    dataframe['author'] = used_authors
    dataframe['gender'] = genders
    dataframe.to_csv("authors.csv")

    # TODO Inform teacher about results
'''
counting_males("authors.csv")