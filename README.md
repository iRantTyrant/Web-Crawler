
# Web Scraper and Text Mining Project

## Author
iRant (ece21168)

## Project Overview
This project is developed as part of the Data-Mine course at the university. It is a web scraper and text mining tool that crawls a website, scrapes the content, processes and cleans it using NLP techniques, stores the data in MongoDB, and provides functionality to index, search, and analyze the content. Additionally, it can create similarity models using Bag of Words (BoW) and TF-IDF, and visualize the similarity results with heatmaps.

## Features
- Crawl websites to extract titles and URLs.
- Scrape webpage content.
- Store scraped data in MongoDB.
- Clean and preprocess text using NLTK.
- Create text indexes and search within MongoDB.
- Generate Bag of Words and TF-IDF similarity matrices.
- Visualize similarity matrices with tables and heatmaps.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- MongoDB installed and running locally or remotely

### Steps to Run

1. **Clone the repository**

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Configure MongoDB connection**

Make sure MongoDB is running on your machine or accessible remotely. The default URI used is:

```plaintext
mongodb://mongoadmin:secret123@localhost:27017/
```

You can change this in the `main.py` file if needed.

5. **Run the program**

```bash
python main.py
```

Follow the interactive menu to crawl, scrape, index, search, clean data, and analyze documents.

## Folder Structure

```
src/
  crawl_scrape_titles_urls.py
  scrape_content.py
  db_store.py
  text_indexing.py
  nltk_handle.py
  bow_handle.py
  tf-idf_handle.py
  visualize.py
main.py
requirements.txt
README.md
```

## Notes
- Ensure NLTK data packages (`punkt`, `stopwords`) are downloaded (the program handles this automatically).
- The visualizations of similarity matrices are saved under the `plots/` folder.
- Cleaned content is saved in MongoDB under the `cleaned_content` field for further analysis.

## Contact
For questions or feedback, please contact: [theflyingtoastgr@gmail.com]

---

Thank you for using this project!
