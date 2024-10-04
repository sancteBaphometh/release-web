from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# для парсинга
import requests
from bs4 import BeautifulSoup

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить любые HTTP-методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить любые заголовки
)


class Release(BaseModel):
    label: str
    version: str
    description: str
    download_url: str


# Получаем HTML-страницу релизов
url = "https://github.com/sancteBaphometh/release-web/releases"
response = requests.get(url)

# Парсим HTML-страницу
soup = BeautifulSoup(response.text, "html.parser")

# Извлекаем список релизов
raw_releases = soup.find_all("div", class_="Box-body")

releases = []

for release in raw_releases:
    label = release.find("span", class_="Label Label--success Label--large").text
    version = release.find("a", class_="Link--primary Link").text
    link = "https://github.com" + release.find("a").get("href")
    text = release.find("div", class_="markdown-body my-3").text
    text = text.split("~")
    description = text[0]
    download = text[1]

    releases.append(
        Release(
            label=label, version=version, description=description, download_url=download
        )
    )


@app.get("/releases")
async def get_releases() -> List[Release]:
    return releases


@app.get("/releases/{release_id}")
async def get_release(release_id: int):
    try:
        release = releases[release_id]
        return release
    except IndexError:
        raise HTTPException(status_code=404, detail="Релиз не найден")


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
