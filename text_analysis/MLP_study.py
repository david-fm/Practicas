import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.activations import sigmoid

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

# Train the model
model.fit(X_train, y_train,
            batch_size=32,
            epochs=5,
            verbose=1,
            validation_split=0.1,
            shuffle=True)


