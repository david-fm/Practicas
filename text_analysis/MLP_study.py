from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.activations import sigmoid
import pandas as pd
from .tf_idf import tf_idf


PATH = "/Users/davidflorezmazuera/Library/CloudStorage/GoogleDrive-270191@student.pwr.edu.pl/Mi unidad/Spanish_V2"

# Create a sequential model that has as input the vectorized text in a dict of 1000 words
# and as output 2 classes (male and female)
model = Sequential()
model.add(Dense(512, input_shape=(1000,)))
model.add(Activation(sigmoid))
model.add(Dropout(0.5))
model.add(Dense(512, input_shape=(1000,)))
model.add(Activation(sigmoid))
model.add(Dropout(0.5))
model.add(Dense(2))
model.add(Activation('softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

# Load the data
dataframe = pd.read_csv("authors.csv")
dataframe = dataframe.dropna()

# Get the tf_idf of the books in 
# get the books
books = []
for book_id in dataframe['book_id']:
    # get the .txt file
    with open(f"{PATH}/{book_id}.txt") as f:
        books.append(tf_idf(f.read()))
    
# define the X and y
x = books
y = dataframe['gender'].values


# Train the model
model.fit(  x, y,
            batch_size=32,
            epochs=5,
            verbose=1,
            validation_split=0.1,
            shuffle=True)


