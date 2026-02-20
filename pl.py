from typing import List, Dict, Any, Optional, Union, cast
import requests
import csv
import os

file_path: str = 'books.csv'
url: str = 'http://openlibrary.org/search.json'


def get_current_page() -> int:
    if not os.path.exists('page.txt'):
        return 1
    with open('page.txt', "r") as f:
        return int(f.read().strip())


def save_page_num(page_num: int) -> None:
    with open('page.txt', "w") as f:
        f.write(str(page_num))


current_page: int = get_current_page()
par: Dict[str, Union[str, int]] = {
    "q": "python",
    "limit": 50,
    "page": current_page,
    "fields": "title,author_name,first_publish_year"
}

response: requests.Response = requests.get(url, params=par)
data: Dict[str, Any] = response.json()

books: List[Dict[str, Any]] = data.get('docs', [])
num_found: int = data.get('num_found', 0)
total_pages: int = (num_found + par['limit'] - 1) // par['limit']

if current_page > total_pages or len(books) == 0:
    print("that was the last page.You will be returned to the first page.")
    save_page_num(1)
    exit()

filtered_books: List[Dict[str, Any]] = list(
    filter(
        lambda book: book.get('first_publish_year', 0) > 2000,
        data['docs']))

output: Optional[Any] = None
writer: Optional[csv.writer] = None

if not os.path.exists(file_path):
    output = open(file_path, mode='w', newline='', encoding='utf-8')
    writer = csv.writer(output)
    writer.writerow(['Title', 'Author', 'Year'])

else:
    output = open(file_path, mode='a', newline='', encoding='utf-8')
    writer = csv.writer(output)

if writer is None:
    raise Exception("error in writer")

for book in filtered_books:
    title: str = book.get('title', 'Not Available')
    author: str = book.get('author_name', ['Not Available'])[
        0] if book.get('author_name') else 'Not Available'
    year: Union[int, str] = book.get('first_publish_year', 'Not Available')
    writer.writerow([title, author, year])

output.close()
print(f"{len(filtered_books)} books were saved to the file.")

save_page_num(current_page + 1)
