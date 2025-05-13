import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os

# Download necessary resources from NLTK
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Preprocesses input text by:
    1. Converting to lowercase
    2. Removing special characters and punctuation
    3. Tokenizing words
    4. Removing stopwords
    """
    if not text:
        return ""
    
    # Convert text to lowercase
    text = text.lower()
    
    # Remove special characters and punctuation
    text = re.sub(f"[{string.punctuation}]", "", text)
    
    # Tokenize text
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    return " ".join(filtered_words)

if __name__ == "__main__":
    sample_text = "Physiotherapy helps in rehabilitation. Exercises improve mobility & reduce pain!"
    processed_text = preprocess_text(sample_text)
    print("Processed Text:", processed_text)
