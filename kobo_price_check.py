"""Check the prices of all books in a list and report any with price £2 or less

Next step is to multithread the requests."""

from pathlib import Path

from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
from tqdm import tqdm


AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0"
MAX_PRICE = 200
WISHLIST = "wishlist.txt"


def get_link(url: str, agent: str = AGENT):
    """Return http response from a given url"""
    headers = {"User-Agent": agent}
    return requests.get(url, headers=headers, allow_redirects=False, timeout=20)


def make_soup(url: str):
    """Get content from a url and parse it with Beautiful Soup."""
    response = get_link(url)
    return BeautifulSoup(response.text, "lxml")


def get_book_details(soup):
    title = soup.find("p", {"class": "sub-section-title"}).text.strip()
    author = soup.find("p", {"class": "book-author"}).text[3:].strip()
    price = (
        soup.find("div", {"class": "active-price"})
        .find("span", {"class": "price"})
        .text.strip()
    )
    cheap = int(price[1:].replace(".", "")) <= MAX_PRICE
    return {"title": title, "author": author, "price": price, "cheap": cheap}


def main():
    with Path(WISHLIST).open("r") as file:
        wishlist = file.readlines()

    cheap_books = []
    for url in tqdm(wishlist):
        soup = make_soup(url.strip())
        try:
            details = get_book_details(soup)
        except AttributeError as error:
            print(f"Failed to get details for '{url}'")
            print(error)
            print()
        if details["cheap"]:
            cheap_books.append(
                (details["title"], details["author"], details["price"], url)
            )

    if cheap_books:
        print(tabulate(cheap_books, headers=["Title", "Author", "Price", "Url"]))
    else:
        print(f"Nothing going for {MAX_PRICE} or less")


if __name__ == "__main__":
    main()
