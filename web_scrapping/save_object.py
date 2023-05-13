import pickle

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    # Open the file in binary mode
    with open(filename, "rb") as f:
        # Load one object from the file
        obj = pickle.load(f)
        return obj
    