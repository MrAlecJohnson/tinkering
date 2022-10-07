"""Check the prices of all books in a list and report any with price £2 or less

Next step is to multithread the requests."""

from concurrent.futures import ThreadPoolExecutor, as_completed
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


def get_price_details(url):
    """Do everything for one url."""
    url = url.strip()
    soup = make_soup(url)
    details = get_book_details(soup)
    details["url"] = url
    return details


def main():
    with Path(WISHLIST).open("r") as file:
        wishlist = file.readlines()

    results = []
    failed = []
    with tqdm(desc="Wishlist books", total=len(wishlist)) as progress_bar:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(get_price_details, url): url for url in wishlist}
        for future in as_completed(futures):
            if future.exception():
                failed.append(futures[future])
            else:
                results.append(future.result())
            progress_bar.update(1)

    cheap_books = [
        (result["title"], result["author"], result["price"], result["url"])
        for result in results
        if result["cheap"]
    ]

    if cheap_books:
        ordered = sorted(cheap_books, key=lambda book: book[1])
        print(tabulate(ordered, headers=["Title", "Author", "Price", "Url"]))
    else:
        print(f"Nothing going for {MAX_PRICE} or less")


if __name__ == "__main__":
    main()
