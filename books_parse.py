import json
import requests
from parsel import Selector, SelectorList
from requests import Response

from utils import WorkWithFiles


class BooksToScrapeParse(WorkWithFiles):
    def __init__(self, url: str, filename: str = "books") -> None:
        self.url = url
        self.headers = self.get_headers()
        self.response = self.make_request()
        self.save_to_html(response=self.response, filename=filename)


    def get_headers(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        }


    def make_request(self) -> Response:
        return requests.get(url=self.url, headers=self.headers)


    def parse_books(self) -> list[dict]:
        data: list[dict] = []

        pag_count = 0

        while True:
            selector: Selector = Selector(text=self.response.text)
            books: SelectorList = selector.css("article.product_pod")[:20]

            for book in books:
                if pag_count == 0: image = self.url + "media" + book.css("img::attr(src)").get()[5:]
                else: image = self.url + "media" + book.css("img::attr(src)").get()[8:]
                title = book.css("h3 a::attr(title)").get().strip()
                if pag_count == 0: link = self.url + "/catalogue/" + book.css("h3 a::attr(href)").get()[10:]
                else: link = self.url + "/catalogue/" + book.css("h3 a::attr(href)").get()
                rating = book.css("p.star-rating::attr(class)").get().split()[-1]
                price = book.css("p.price_color::text").get().strip()[1:]
                stock = "In stock" if "In stock" in book.css("p.availability::text").get() else "Out of stock"
                position = books.index(book) + 1 + (pag_count * 20)

                data.append({
                    "image": image,
                    "title": title,
                    "link": link,
                    "rating": rating,
                    "price": price,
                    "stock": stock,
                    "position": position
                })

            next_button: str = selector.css('.pager .next a::attr(href)').get()
            if next_button:
                url: str = self.url + next_button
                self.response = requests.get(url=url, headers=self.headers)
                pag_count += 1
            else:
                break

        return data


    def print(self, data: list[dict]) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))
