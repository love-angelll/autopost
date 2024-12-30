```
autoposting
├── main
│   ├── LICENSE           # Project License
│   ├── main.py           # Basic Logic 
│   ├── .env              # Configuration file for API credentials
│   ├── Примеры           # Examples of bot work
├── requirements.txt      # Required libraries for the project
└── README.md             # Project Documentation
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
python app.py
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




