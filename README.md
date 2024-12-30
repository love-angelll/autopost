<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

# [RU] Бот для автоматической публикации сообщений из Telegram в ВКонтакте

Этот проект представляет собой скрипт на Python, который автоматически публикует сообщения из Telegram-канала или чата в указанную группу ВКонтакте. Он поддерживает различные типы контента, включая текст, изображения, видео и ссылки.

# Содержание RU
1. [Зачем нужен?](#зачем-нужен-этот-проект)
2. [Как работает?](#как-работает-скрипт)
3. [Структура проекта](#структура-проекта)
4. [Какие медиафайлы может пересылать?](#какие-медиафайлы-может-пересылать-бот)
5. [Пример использования](#пример-использования)
6. [Установка и запуск проекта](#установка-и-запуск-проекта)
7. [Подробности реализации](#подробности-реализации)
8. [Особенности](#особенности)
9. [Содействие](#содействие)

## Зачем нужен этот проект

Многие пользователи и администраторы сообществ сталкиваются с необходимостью дублирования контента между различными платформами. Это может быть рутинной и трудоемкой задачей. Данный скрипт автоматизирует этот процесс, экономя время и уменьшая вероятность ошибок при копировании данных вручную.

## Как работает скрипт

1. **Получение данных из Telegram:** Проект использует библиотеку `aiogram` для взаимодействия с Telegram API. Это позволяет получать сообщения и медиафайлы из указанных чатов или каналов.
2. **Обработка медиа-контента:** С помощью `aiogram-media-group`, `moviepy` и `rlottie-python` происходит обработка и подготовка медиафайлов для дальнейшей отправки.
3. **Отправка данных в ВКонтакте:** Библиотека `vk-api` используется для взаимодействия с API ВКонтакте, что позволяет загружать и отправлять медиафайлы и сообщения на указанные страницы или группы.
4. **Конфигурация и управление:** Файл `.env` используется для хранения конфиденциальных данных и ключей API, обеспечивая безопасное управление параметрами приложения.

## Структура проекта

```
autoposting
├── main
│   ├── main.py           # Основная логика
│   ├── .env              # Файл конфигурации для учетных данных API
├── requirements.txt      # Необходимые библиотеки для проекта
├── EXAMPLES              # Примеры проекта
├── LICENSE               # Лицензия на проект
└── README.md             # Проектная документация
```

## Какие медиафайлы может пересылать бот

Бот предназначен для пересылки различных типов медиафайлов из Telegram в ВКонтакте. Вот список медиафайлов, которые бот может обрабатывать и пересылать:

1. **Текстовые сообщения**:
   - Простые текстовые сообщения без медиафайлов.
2. **Изображения**:
   - Фотографии в различных форматах (JPEG, PNG и др.).
3. **Видео**:
   - Видеофайлы в популярных форматах (MP4 и др.).
4. **Аудио**:
   - Голосовые сообщения и музыкальные файлы.
5. **Документы**:
   - Файлы различных типов, включая PDF, DOCX, XLSX и другие.
6. **Анимации**:
   - GIF-анимации и анимированные стикеры.
7. **Медиа-группы**:
   - Группы медиафайлов, включающие комбинации изображений и видео, отправленные как единое сообщение.

## Пример использования

- **Изображения**: Если пользователь отправляет в Telegram фото с описанием, бот автоматически пересылает это изображение и текст на указанную страницу или группу ВКонтакте.
- **Видео**: Видео с Telegram пересылается в соответствующем формате в ВКонтакте, сохраняя оригинальное качество.
- **Документы**: Важные файлы или документы пересылаются для удобного доступа участников группы ВКонтакте.
- **Голосовые сообщения**: Голосовые записи из Telegram пересылаются как аудиофайлы в ВКонтакте.

Таким образом, скрипт поддерживает широкий спектр медиафайлов, обеспечивая гибкость и удобство при переносе контента между платформами. 

## Установка и запуск проекта

1. **Склонируйте репозиторий:**

   ```bash
   git clone https://github.com/love-angelll/autopost
   cd autopost
   ```

2. **Установите необходимые зависимости:**

   Убедитесь, что у вас установлен `pip`. Затем выполните команду:

   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка окружения:**

   Создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения. Пример файла `.env`:

   ```env
   VK_API_TOKEN=YOUR_VK_API_TOKEN
   TELEGRAM_API_TOKEN=YOUR_TELEGRAM_API_TOKEN
   TELEGRAM_CHANNEL_USERNAME=YOUR_TELEGRAM_CHANNEL_USERNAME
   VK_GROUP_ID=YOUR_VK_GROUP_ID
   ```

4. **Запуск приложения:**

   Приложение можно запустить с помощью следующей команды:

   ```bash
   python main.py
   ```

## Подробности реализации

- **`aiogram`**: Асинхронная библиотека для работы с Telegram Bot API.
- **`aiogram-media-group`**: Расширение для обработки групповых медиа-сообщений в Telegram.
- **`aiohttp`**: Асинхронная библиотека HTTP-клиента/сервера.
- **`python-dotenv`**: Позволяет загружать переменные окружения из файла `.env`.
- **`vk-api`**: Библиотека для работы с API ВКонтакте.
- **`rlottie-python`**: Библиотека для работы с анимациями.
- **`moviepy`**: Библиотека для редактирования видео.

## Особенности

- Поддерживает публикацию текстовых сообщений, изображений, видео и ссылок.
- Настраивается с помощью простого файла TOML.
- Регистрирует активность, что помогает в отладке и мониторинге.

## Содействие

Не стесняйтесь отправлять проблемы или запросы на исправление, если у вас есть какие-либо вопросы то пишите в соц. сетях.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/iv_frunza)
[![VK Основной](https://img.shields.io/badge/VK%20Основной-4A76A8?style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/iv.frunza)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/iv.frunza)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# [EN] Bot for Automatic Posting from Telegram to VKontakte

This project is a Python script that automatically posts messages from a Telegram channel or chat to a specified VKontakte group. It supports various content types, including text, images, videos, and links.

## Why is this project useful?

Many users and community administrators face the need to duplicate content across different platforms. This can be a routine and time-consuming task. This script automates the process, saving time and reducing the risk of errors when copying data manually.

## How does the script work?

1. **Retrieving data from Telegram:** The project uses the `aiogram` library to interact with the Telegram API. This allows retrieving messages and media files from specified chats or channels.
2. **Processing media content:** Libraries such as `aiogram-media-group`, `moviepy`, and `rlottie-python` are used to process and prepare media files for further posting.
3. **Sending data to VKontakte:** The `vk-api` library interacts with VKontakte API, enabling uploading and posting of media files and messages to specified pages or groups.
4. **Configuration and management:** A `.env` file is used to store sensitive data and API keys, ensuring secure application settings management.

## Project Structure

```
autoposting
├── main
│   ├── main.py           # Main logic
│   ├── .env              # Configuration file for API credentials
├── requirements.txt      # Required libraries for the project
├── EXAMPLES              # Project examples
├── LICENSE               # Project license
└── README.md             # Project documentation
```

## What types of media can the bot forward?

The bot is designed to forward various types of media from Telegram to VKontakte. Here's a list of media types the bot can process and forward:

1. **Text messages**:
   - Simple text messages without media.
2. **Images**:
   - Photos in various formats (JPEG, PNG, etc.).
3. **Videos**:
   - Video files in popular formats (MP4, etc.).
4. **Audio**:
   - Voice messages and music files.
5. **Documents**:
   - Files of various types, including PDF, DOCX, XLSX, and others.
6. **Animations**:
   - GIF animations and animated stickers.
7. **Media groups**:
   - Groups of media files, including combinations of images and videos sent as a single message.

### Example Usage

- **Images**: If a user sends a photo with a description in Telegram, the bot automatically forwards the image and text to the specified VKontakte page or group.
- **Videos**: Videos from Telegram are forwarded in the appropriate format to VKontakte, preserving the original quality.
- **Documents**: Important files or documents are forwarded for easy access by VKontakte group members.
- **Voice messages**: Voice recordings from Telegram are forwarded as audio files to VKontakte.

Thus, the script supports a wide range of media files, ensuring flexibility and convenience when transferring content between platforms.

## Installation and Launch

### 1. **Clone the repository:**

   ```bash
   git clone https://github.com/love-angelll/autopost
   cd autopost
   ```

### 2. **Install dependencies:**

Ensure pip is installed, then execute:
```
pip install -r requirements.txt
```

### 3. Set up the environment:

Create a .env file in the project root and add the required environment variables. Example .env file:
```env
VK_API_TOKEN=YOUR_VK_API_TOKEN
TELEGRAM_API_TOKEN=YOUR_TELEGRAM_API_TOKEN
TELEGRAM_CHANNEL_USERNAME=YOUR_TELEGRAM_CHANNEL_USERNAME
VK_GROUP_ID=YOUR_VK_GROUP_ID
```

### 4. Run the application:

Launch the app with the following command:
```
python main.py
```


#### Implementation Details

- **`aiogram:`** Asynchronous library for Telegram Bot API.
- **`aiogram-media-group:`** Extension for handling Telegram  media group messages.
- **`aiohttp:`** Asynchronous HTTP client/server library.
- **`python-dotenv:`** Loads environment variables from the .env file.
- **`vk-api:`** Library for VKontakte API.
- **`rlottie-python:`** Library for working with animations.
- **`moviepy:`** Library for video editing.


## Features

- Supports posting of text messages, images, videos, and links.
- Configurable through a simple TOML file.
- Logs activity, aiding in debugging and monitoring.


## Contribution

Feel free to submit issues or pull requests. If you have any questions, contact me via social media.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/iv_frunza)
[![VK Основной](https://img.shields.io/badge/VK%20Основной-4A76A8?style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/iv.frunza)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/iv.frunza) 


