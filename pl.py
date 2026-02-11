import requests
import json

url = 'http://openlibrary.org/search.json'

par = {
    "q" : "law",
    "limit" : 50,
    "fields" : "title,author_name,first_publish_year"
    }

response = requests.get(url,params=par)
data = response.jason()
books_after_2000 = list(filter(lambda book: book.get('first_publish_year', 0) > 2000, data['docs']))

