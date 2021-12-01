import requests

from pathlib import Path


def get_local_input(filename, as_list=True):
    with open(Path("data") / filename) as f:
        if as_list:
            return [line.strip() for line in f.readlines()]
        else:
            return f.read()


def load_cookie():
    with open(Path.cwd().parent.parent / "creds/cookie.txt", "r") as cookie:
        return cookie.readline()


def get_online_input(url, filename):
    cookie = load_cookie()
    response = requests.get(url, cookies={"session": cookie})
    if response.ok:
        with open(Path("data") / filename, "w") as f:
            f.write(response.text)

            
def get_input(day: int):
    get_online_input(f"https://adventofcode.com/2020/day/{day}/input", f"inputs_{day}.txt")