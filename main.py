#Importing necessary libraries
from src.crawl_scrape_titles_urls import crawl_web #Importing the function to crawl the website and extract titles and URLs
from src.scrape_content import scrape_web #Importing the function to scrape content from the web
from src.db_store import store_to_mongo #Importing the function to store data in MongoDB
from src.text_indexing import create_text_index_and_search #Importing the function to create a text index and search in MongoDB
from src.nltk_handle import nltk_handle #Importing the function to handle NLTK operations
import pymongo #Importing the pymongo library to interact with MongoDB
from pymongo import MongoClient #Importing MongoClient to connect to MongoDB
import os#Importing the os library to handle file paths and environment variables
import nltk #Importing the NLTK library for natural language processing
from src.bow_handle import create_bow_and_compare #Importing the function to create a Bag of Words (BoW) model and compare documents
from src.tf_idf_handle import create_tfidf_and_compare #Importing the function to create a TF-IDF model and compare documents
from src.visualize import visualize_similarity #Importing the function to visualize the similarity matrix

#URI for MongoDB 
uri = "mongodb://mongoadmin:secret123@localhost:27017/"

#Database name
db_name = "web_data"

#Collection name
collection_name = "web_content"

#Url of the website to crawl
url = 'https://worldadventuredivers.com/'

#Here we will store in JSON format the data we will scrape so we can store it in MongoDB
enriched_content = []

# Print the titles and links
loop = 1

#Initialize the NLTK components
nltk.download('punkt')
nltk.download('stopwords')

#Welcome message
print("\nWelcome to the Web Scraper")
print("This program will crawl a website, scrape the content, and store it in MongoDB.Also you can index the data and search it and mine for content.")

#Default value for user input to ask if they want to continue
user_main = "yes"

#While loop to ask the user if they want to continue it works as long as the user inputs "yes"
while (user_main == "yes"):

    #Main menu to ask the user what they want to do 
    print("\nMain Menu:")
    print("1. Continue to scrape the content")
    print("2. Index the data and search it")
    print("3. Use NLTK to clean the data")
    print("4. Create Bag Of Words (BOW) and compare all the documents in the collection")
    print("5. Create a TF-IDF (Term Frequency-Inverse Document Frequency) model and compare all the documents in the collection")
    print("6. Exit the program")

    #Ask the user to enter their choice
    print("\nPlease enter your choice (1/2/3/4/5/6): ")
    menu_choice = input().strip()

    #If the user inputs 1, we will continue to scrape the content
    if (menu_choice == '1'):
        print("You chose to continue to scrape the content.")

        #Call the function to crawl the website
        titles = crawl_web(url)

        #For loop for the web crawl and the scraping of the content
        for title, link in titles:
            #Print empty line for better readability
            print("\n")

            #Print the title and link
            print(f"\n {loop} Title: {title}, Link: {link}")

            #Mine the web page for content
            content = scrape_web(link)

            #Print the content
            print(f"\n {loop} Content: {content}")

            #Add the title and content to the enriched_content list in JSON format
            enriched_content.append({
                "title": title,
                "link": link,
                "content": content
            })

            #Increment the loop counter
            loop += 1

        #Store the data in MongoDB
        store_to_mongo(enriched_content, db_name, collection_name, uri)

        #Ask if the user wants to go back to the main menu
        user_main = input("\nDo you want to go back to the main menu? (yes/no): ").strip().lower()


    elif menu_choice == '2':
        print("You chose to index the data and search it.")
        #Default value for user input to ask if they want to index the data
        user_input = "yes"

        #While loop to ask the user if they want to index the data it works as long as the user inputs "yes"
        while user_input == "yes":

            #Ask the user if they want to index the data
            user_input = input("Do you want to index the data? (yes/no): ").strip().lower()

            #If the user inputs "yes", we will create a text index and search the data
            if (user_input == 'yes'):

                #Ask the user for the search term
                user_index = input("Enter the search term (or press Enter for default): ").strip()
                
                #Create text index and search
                create_text_index_and_search(user_index if user_index else None, uri, db_name, collection_name)

            #If the user inputs "no", we will exit the program
            else:
                print("Indexing skipped. Exiting the indexing & searching.")
        #Ask if the user wants to go back to the main menu
        user_main = input("\nDo you want to go back to the main menu? (yes/no): ").strip().lower()

    #If the user inputs 3, we will exit the program        
    elif menu_choice == '3':

        print("You chose to use NLTK to clean the data.")

        #Connect to MongoDB
        print("🔗 Connecting to MongoDB...")
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]

        #Get all documents from MongoDB
        documents = collection.find()

        #For each document, we will process the content using NLTK
        for doc in documents:

            #Get the content from the document
            content = doc.get('content', '')

            #Check if content is not empty
            if content:

                #Use the nltk_handle function to process the content
                print(f"\nProcessing content for document ID: {doc['_id']}")
                tokens = nltk_handle(content)

                #Join the tokens back into a single string
                cleaned_text = " ".join(tokens)
                
                #Print the cleaned text for debugging purposes
                print(f"\nCleaned Content: {cleaned_text}")
                
                #Update the document with a new field 'cleaned_content' which contains the cleaned text
                result = collection.update_one(
                    {'_id': doc['_id']},
                    {'$set': {'cleaned_content': cleaned_text}}
                )
                print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

        #Print a message to indicate that the NLTK processing is completed
        print("\nNLTK processing completed. Cleaned content stored in MongoDB.")

        #Ask if the user wants to go back to the main menu
        user_main = input("\nDo you want to go back to the main menu? (yes/no): ").strip().lower()
        #Close the MongoDB connection
        client.close()
        print("\n🔗 Connection to MongoDB closed.")

    #If the user inputs 4, we will create a Bag Of Words (BOW) model and compare all the documents in the collection
    elif menu_choice == '4':        
        #Connect to MongoDB
        print("\n🔗Connecting to MongoDB...")
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"Connected to database: {db_name}, collection: {collection_name}")

        #Get all cleaned content from the documents from the collection
        documents_cursor = collection.find({"cleaned_content": {"$exists": True}})

        #Make them into a list 
        documents = [doc['cleaned_content'] for doc in documents_cursor if doc.get('cleaned_content')]
        
        #If there are no documents with 'cleaned_content', we will print a message
        if not documents:
            print("No documents with 'cleaned_content' found in the collection.")
            client.close()    
            print("\n🔗Connection to MongoDB closed.")
            continue # Exit the loop and go back to the main menu
        
        #Call the function to create a Bag of Words (BoW) model and compare all the documents in the collection
        similarity_matrix = create_bow_and_compare(documents)

        #Print the similarity matrix
        if similarity_matrix is not None:
            print("\nCosine Similarity Matrix:")
            print(similarity_matrix)
        else:
            print("No documents to compare.")

        #Visualize the similarity matrix
        labels = [f'Doc {i}' for i in range(len(documents))]
        print("\nVisualizing the similarity matrix...")

        visualize_similarity(similarity_matrix, labels=labels, filename='plots/similarity_visualization-bow.png', fontsize=10)
        print("\nSimilarity matrix visualization saved as 'plots/similarity_visualization-bow.png'.")
        
        #Ask if the user wants to go back to the main menu
        user_main = input("\nDo you want to go back to the main menu? (yes/no): ").strip().lower()
    
    #If the user inputs 5, we will create a TF-IDF model and compare all the documents in the collection
    elif menu_choice == '5':
        #Connect to MongoDB
        print("\n🔗Connecting to MongoDB...")
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        print(f"Connected to database: {db_name}, collection: {collection_name}")

        #Get all cleaned content from the documents from the collection
        documents_cursor = collection.find({"cleaned_content": {"$exists": True}})

        #Make them into a list 
        documents = [doc['cleaned_content'] for doc in documents_cursor if doc.get('cleaned_content')]
        
        #If there are no documents with 'cleaned_content', we will print a message
        if not documents:
            print("No documents with 'cleaned_content' found in the collection.")
            client.close()    
            print("\n🔗Connection to MongoDB closed.")
            continue # Exit the loop and go back to the main menu
        
        #Call the function to create a TF-IDF model and compare all the documents in the collection
        similarity_matrix = create_tfidf_and_compare(documents)

        #Print the similarity matrix
        if similarity_matrix is not None:
            print("\nCosine Similarity Matrix:")
            print(similarity_matrix)
        else:
            print("No documents to compare.")
        
        #Visualize the similarity matrix
        labels = [f'Doc {i}' for i in range(len(documents))]
        print("\nVisualizing the similarity matrix...")
        
        visualize_similarity(similarity_matrix, labels=labels, filename='plots/similarity_visualization-tf-idf.png', fontsize=10)
        
        print("\nSimilarity matrix visualization saved as 'plots/similarity_visualization-tf-idf.png'.")
        
        #Ask if the user wants to go back to the main menu
        user_main = input("\nDo you want to go back to the main menu? (yes/no): ").strip().lower()

    #If the user inputs 6 we will exit the program
    elif menu_choice == '6':
        print("Exiting the program. Goodbye!")
        user_main = "no"    
    
    #If the user inputs an invalid choice, we will print an error message
    else:
        print("\nInvalid choice. Please enter 1, 2, 3, 4, 5, 6.")

#End of the main script