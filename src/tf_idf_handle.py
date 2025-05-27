#Importing necessary libraries
from sklearn.feature_extraction.text import TfidfVectorizer  # Importing TfidfVectorizer to create a TF-IDF model
from sklearn.metrics.pairwise import cosine_similarity  # Importing cosine_similarity to calculate similarity between documents
def create_tfidf_and_compare(documents):
    """
    This function creates a TF-IDF (Term Frequency-Inverse Document Frequency) model from the documents
    and compares the documents using cosine similarity. It returns a similarity matrix.
    
    :param documents: List of documents (strings) to be processed
    :return: Similarity matrix as a 2D array
    """
    
    # Create a TfidfVectorizer instance
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the documents to create the TF-IDF model
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Print TF-IDF Dictionary for debugging purposes
    print("TF-IDF Dictionary:")
    print(vectorizer.get_feature_names_out())

    # Print TF-IDF Frequency Matrix for debugging purposes
    print("\nTF-IDF Frequency Matrix:")
    print(tfidf_matrix.toarray())
    
    # Calculate cosine similarity between the documents
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    return similarity_matrix