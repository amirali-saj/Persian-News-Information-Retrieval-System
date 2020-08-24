# Persian-News-Information-Retrieval-System (سیستم بازیابی اطلاعات اخبار فارسی)
An Information retrieval system for Persian news with ranked retrieval of documents according to relevance to the query.

## Ranked Retrieval
Ranked retrieval uses tf-idf vectors to represent documents and queires and calculates similarity between queries and documents using cosine similarity. News are retrieved from inverted indices constructed from dataset collections. Champions lists are used to improve system search speed.

## Text Processing
- Removing persian sotp words using persian stop words dataset provided by [https://github.com/kharazi/persian-stopwords]
- Normalizing text
- Smart Stemming for persian verbs and nouns
- Handling compound terms
