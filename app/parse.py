import requests
from bs4 import BeautifulSoup
import csv
from dataclasses import dataclass


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def scrape_quotes() -> list[Quote]:
    quotes = []
    page = 1
    while True:
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_blocks = soup.select(".quote")

        if not quote_blocks:
            break

        for block in quote_blocks:
            text = block.select_one(".text").get_text(strip=True)
            author = block.select_one(".author").get_text(strip=True)
            tags = [
                tag.get_text(strip=True)
                for tag in block.select(".tags .tag")
            ]
            quotes.append(Quote(text=text, author=author, tags=tags))

        page += 1

    return quotes


def main(output_csv_path: str) -> None:
    quotes = scrape_quotes()
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "author", "tags"])
        for qts in quotes:
            writer.writerow([qts.text, qts.author, ",".join(qts.tags)])


if __name__ == "__main__":
    main("quotes.csv")
