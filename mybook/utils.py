
import requests

def get_book_cover_info(isbn):
    api_url = f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        
        if f'ISBN:{isbn}' in data:
            cover_info = data[f'ISBN:{isbn}']['cover']
            return cover_info
    return None
