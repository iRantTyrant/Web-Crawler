#Import necessary libraries
from sklearn.feature_extraction.text import CountVectorizer# Importing CountVectorizer to create a Bag of Words model
from sklearn.metrics.pairwise import cosine_similarity # Importing cosine_similarity to calculate similarity between documents


def create_bow_and_compare(documents):
    """
    This function creates a Bag of Words (BoW) model from the documents in the MongoDB collection
    and compares the documents using cosine similarity. It returns a similarity matrix.

    """
    
    # Create a CountVectorizer instance
    vectorizer = CountVectorizer()
    
    # Fit and transform the documents to create the BOW model
    bow_matrix = vectorizer.fit_transform(documents)

    #Print BOW Dictionary for debugging purposes
    print("BoW-Dictionary:")
    print(vectorizer.get_feature_names_out())

    #Print BOW Frequency Matrix for debugging purposes
    print("\nBoW- Frequency Matrix :")
    print(bow_matrix.toarray())
    
    # Calculate cosine similarity between the documents
    similarity_matrix = cosine_similarity(bow_matrix)
    
    return similarity_matrix