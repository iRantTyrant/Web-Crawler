#Importing necessary libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

"""

"""

def nltk_handle(text):

    #NLTK PIPELINE

    #1. Tokenization (we split the text into individual words)
    tokens = word_tokenize(text)

    #2. Stopword Removal (we remove common words that do not contribute to the meaning of the text ex. "the", "is", "in", etc.)
    filtered_tokens = [word for word in tokens if word.lower() not in stopwords.words('english') and word.isalpha()]

    #3. Stemming (reducing words to their root form)
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(word) for word in filtered_tokens]
    
    #Return the processed tokens
    return stemmed_tokens