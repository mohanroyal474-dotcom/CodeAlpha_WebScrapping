import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"
books = []

while url:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        rating_classes = book.select_one(
            ".star-rating"
        ).get("class", [])

        books.append({
            "Title": book.h3.a["title"],
            "Price": book.select_one(
                ".price_color"
            ).get_text(strip=True),
            "Rating": (
                rating_classes[1]
                if len(rating_classes) > 1
                else "Unknown"
            ),
            "Availability": book.select_one(
                ".availability"
            ).get_text(" ", strip=True),
            "Product_URL": urljoin(
                url, book.h3.a["href"]
            )
        })

    next_page = soup.select_one("li.next a")
    url = (
        urljoin(url, next_page["href"])
        if next_page else None
    )

df = pd.DataFrame(books)
df.to_csv("books.csv", index=False)

print("Scraping completed!")
print("Total books:", len(df))
print(df.head())
print("Saved dataset as books.csv")