# для парсинга
import requests
from bs4 import BeautifulSoup

# Получаем HTML-страницу профиля пользователя
url = "https://github.com/ValdikSS/GoodbyeDPI/releases"
response = requests.get(url)

# Парсим HTML-страницу
soup = BeautifulSoup(response.text, "html.parser")

# Извлекаем список релизов
releases = soup.find_all("div", class_="Box-body")


# Печатаем имена релизов
for release in releases:
    version = release.find("a", class_="Link--primary Link").text
    description = release.find("div", class_="markdown-body my-3").text
    link = "https://github.com" + release.find("a").get("href")

    # Находим ссылку на скачивание в текущем релизе
    download_link_element = soup.find("div", class_="Box-footer").find(
        "summary", role="button"
    )
    # download_link = "https://github.com" + download_link_element.get("href")

    print(download_link_element)
