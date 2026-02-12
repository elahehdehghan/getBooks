import requests
import csv
import os

file_path = 'books.csv'
url = 'http://openlibrary.org/search.json'

def get_current_page():
     if not os.path.exists('page.txt'):
        return 1
     with open('page.txt', "r") as f:
        return int(f.read().strip())
 
def save_page_num(page_num):
    with open('page.txt', "w") as f:
        f.write(str(page_num))
    
current_page = get_current_page()   
par = {
    "q" : "python",
    "limit" : 50,
    "page" : current_page,
    "fields" : "title,author_name,first_publish_year"
    }

response = requests.get(url,params=par)
data = response.json()

books = data.get('docs', [])
num_found = data.get('num_found',0)
total_pages = (num_found + par['limit'] - 1) // par['limit']

if current_page > total_pages or len(books) == 0:
    print("that was the last page.You will be returned to the first page.")
    save_page_num(1)
    exit()

filtered_books = list(filter(lambda book: book.get('first_publish_year', 0) > 2000, data['docs']))

if not os.path.exists(file_path) :
    output = open(file_path, mode='w',newline='', encoding='utf-8') 
    writer = csv.writer(output) 
    writer.writerow(['Title', 'Author', 'Year']) 
    
else :
    output = open(file_path, mode='a',newline='', encoding='utf-8')
    writer = csv.writer(output)

for book in filtered_books:
    title = book.get('title', 'Not Available')
    author = book.get('author_name', ['Not Available'])[0] if book.get('author_name') else 'Not Available'
    year = book.get('first_publish_year', 'Not Available')
    writer.writerow([title, author, year])

output.close() 
print(f"{len(filtered_books)} books were saved to the file.")

save_page_num(current_page + 1)