// Функция для отправки запроса и обработки ответа
function fetchReleases() {
    fetch('http://127.0.0.1:8000/releases', {
        method: 'GET',  // Метод запроса
        headers: {
            'Content-Type': 'application/json',  // Указываем тип контента
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Парсим ответ как JSON
        })
        .then(data => {
            populateTable(data);  // Передаем данные в функцию для заполнения таблицы
        })
        .catch(error => {
            console.error('Fetch error:', error);  // Ловим и выводим ошибки
        });
}

// Функция для заполнения таблицы данными
function populateTable(releases) {
    const tableBody = document.querySelector('#releasesTable tbody');
    tableBody.innerHTML = '';  // Очищаем таблицу перед вставкой новых данных

    releases.forEach(release => {
        const row = document.createElement('tr');

        // Создаем ячейки для каждой колонки
        const labelCell = document.createElement('td');
        labelCell.textContent = release.label;
        row.appendChild(labelCell);

        const versionCell = document.createElement('td');
        versionCell.textContent = release.version;
        row.appendChild(versionCell);

        const descriptionCell = document.createElement('td');
        descriptionCell.textContent = release.description;
        row.appendChild(descriptionCell);

        // Создаем кнопку "Download"
        const downloadCell = document.createElement('td');
        const button = document.createElement('button');
        button.textContent = "Скачать APK";

        // Устанавливаем ссылку на кнопке
        button.addEventListener('click', () => {
            window.location.href = release.download_url;
        });

        downloadCell.appendChild(button);
        row.appendChild(downloadCell);

        // Добавляем строку в тело таблицы
        tableBody.appendChild(row);
    });
}

// Вызов функции для запроса при загрузке страницы
window.onload = fetchReleases;
