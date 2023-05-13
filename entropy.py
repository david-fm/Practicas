from math import log

def entropy(text, n):
    """Calculate the entropy of a text
    :param text: Text to calculate the entropy
    :param n: Number of characters to group
    :return: Entropy of the text"""
    # Calculate the frequency of each group of characters
    freq = {}
    for i in range(len(text) - n):
        group = text[i:i + n]
        freq[group] = freq.get(group, 0) + 1
    # Calculate the entropy
    entropy = 0
    for group in freq:
        p = freq[group] / len(text)
        entropy -= p * log(p, 2)
    return entropy

if __name__ == "__main__":
    # Get the text
    text = open('Maria_Texto_impreso_.txt', 'r').read()
    # Calculate the entropy
    print(entropy(text, 2))