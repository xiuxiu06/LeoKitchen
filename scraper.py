import requests
from bs4 import BeautifulSoup


def scrape_dishes():
    url = "https://www.allrecipes.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dishes = []
    for item in soup.select(".card__detailsContainer"):
        name = item.select_one(".card__title").text.strip()
        image = item.select_one("img")["src"]
        recipe = item.select_one(".card__summary").text.strip()

        dish = {
            "name": name,
            "image": image,
            "calories": "Unknown",
            "recipe": recipe,
            "category": "General"
        }
        dishes.append(dish)

    return dishes
