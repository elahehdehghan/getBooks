import requests
import csv

url = 'http://openlibrary.org/search.json'

par = {
    "q" : "law",
    "limit" : 50,
    "fields" : "title,author_name,first_publish_year"
    }

response = requests.get(url,params=par)
data = response.jason()
filtered_books = list(filter(lambda book: book.get('first_publish_year', 0) > 2000, data['docs']))

output = open('books.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(output)
writer.writerow(['Title', 'Author', 'Year'])

for book in filtered_books:
    title = book.get('title', 'Not Available')
    author = book.get('author_name', ['Not Available'])[0] if book.get('author_name') else 'Not Available'
    year = book.get('first_publish_year', 'Not Available')
    writer.writerow([title, author, year])

output.close() 
print(f"{len(filtered_books)} books were saved to the file.")