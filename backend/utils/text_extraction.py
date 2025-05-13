import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """
    Extracts text content from a given research paper URL using BeautifulSoup.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        
        extracted_text = " ".join(p.get_text() for p in paragraphs)
        
        return extracted_text.strip()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the research paper: {str(e)}"
