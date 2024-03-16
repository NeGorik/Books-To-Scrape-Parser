from books_parse import BooksToScrapeParse


def main() -> None:
    btsp = BooksToScrapeParse(url='https://books.toscrape.com/')
    books_to_scrape_data: list[dict] = btsp.parse_books()
    btsp.print(books_to_scrape_data)


if __name__ == '__main__':
    main()
