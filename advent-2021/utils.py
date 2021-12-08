from pathlib import Path

import requests

def load_cookie() -> None:
    with open(Path.cwd().parent.parent / "cookie.txt", "r") as cookie:
        return cookie.readline()


def get_online_input(url: str, filename: str) -> None:
    cookie = load_cookie()
    response = requests.get(url, cookies={"session": cookie})
    if response.ok:
        with open(Path("data") / filename, "w") as f:
            f.write(response.text)
        print("Data saved")
    else:
        print(f"Response not okay: {response.ok}")


def get_input(day: int):
    get_online_input(f"https://adventofcode.com/2021/day/{day}/input", f"inputs_{day}.txt")


def load_data(
    filename,
    list_type: str = "line",
    number: bool = False,
):
    """List_type can be 'line', 'comma' or 'none'."""
    if isinstance(filename, int):
        filename = f"inputs_{filename}.txt"
    with open(Path("data") / filename) as f:
        if list_type == "line" and number:
            return [int(line.strip()) for line in f.readlines()]
        elif list_type == "comma" and number:
            return [int(num.strip()) for num in f.read().split(",")]
        elif list_type == "line":
            return [line.strip() for line in f.readlines()]
        elif list_type == "comma":
            return [text.strip() for text in f.read().split(",")]
        elif number:
            return int(f.read())
        return f.read()
