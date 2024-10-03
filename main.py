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
    name: str
    version: str
    download_url: str


# Получаем HTML-страницу профиля пользователя
# url = "https://github.com/ValdikSS/GoodbyeDPI/releases"
url = "https://github.com/sancteBaphometh"
response = requests.get(url)

# Парсим HTML-страницу
soup = BeautifulSoup(response.text, "html.parser")

# Извлекаем список релизов
repositories = soup.find_all("li", class_="repo-list-item")

# Печатаем имена релизов
for repository in repositories:
    print(repository)  # .find("a").text)


releases = [
    {
        "name": "My Android App",
        "version": "1.0.0",
        "download_url": "z",
    },
    {
        "name": "My Android App",
        "version": "1.1.0",
        "download_url": "o",
    },
]


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
