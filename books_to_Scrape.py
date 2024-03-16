import json
import requests
from parsel import Selector
from requests import Response

def parse_books(response: Response) -> list[dict]:
    selector = Selector(response.text)
    data = []

    books = selector.css("article.product_pod")[:20]
    for book in books:
        image = response.url + "media" + book.css("img::attr(src)").get()[5:]
        title = book.css("h3 a::attr(title)").get().strip()
        link = response.url + "/catalogue/" + book.css("h3 a::attr(href)").get()[10:]
        rating = book.css("p.star-rating::attr(class)").get().split()[-1]
        price = book.css("p.price_color::text").get().strip()[1:]
        stock = "In stock" if "In stock" in book.css("p.availability::text").get() else "Out of stock"
        position = books.index(book) + 1

        data.append({
            "image": image,
            "title": title,
            "link": link,
            "rating": rating,
            "price": price,
            "stock": stock,
            "position": position
        })

    return data

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
}

url = 'https://books.toscrape.com'
response = requests.get(url=url, headers=headers)

books_data = parse_books(response)
print(json.dumps(books_data, indent=2, ensure_ascii=False))


