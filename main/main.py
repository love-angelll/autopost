import os
import logging
from telethon import TelegramClient, events
import vk_api
from vk_api import VkUpload
from settings import api_id, api_hash, bot_token, channel_id, token, group_id

# Настройка логирования
logging.basicConfig(filename="logs.log", level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Инициализация Telegram-клиента
telegram_client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Инициализация VK-клиента
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
vk_upload = VkUpload(vk_session)

# Папка для временного хранения файлов
TEMP_FOLDER = "files"
os.makedirs(TEMP_FOLDER, exist_ok=True)

async def upload_to_vk(message):
    """Функция для публикации сообщения в группу ВКонтакте"""
    try:
        attachments = []

        # Обработка изображений
        if message.photo:
            file_path = await message.download_media(file=TEMP_FOLDER)
            photo = vk_upload.photo_wall(photos=[file_path], group_id=group_id)
            attachments.append(f"photo{photo[0]['owner_id']}_{photo[0]['id']}")
            os.remove(file_path)

        # Обработка видео
        elif message.video:
            file_path = await message.download_media(file=TEMP_FOLDER)
            video = vk_upload.video(video_file=file_path, group_id=group_id, name=message.text or "Video")
            attachments.append(f"video{video['owner_id']}_{video['video_id']}")
            os.remove(file_path)

        # Формирование текста сообщения
        text = message.text or ""

        # Публикация в группу ВКонтакте
        vk.wall.post(owner_id=f"-{group_id}", message=text, attachments=",".join(attachments))
        logger.info(f"Message posted to VK: {text}")

    except Exception as e:
        logger.error(f"Error posting message to VK: {e}")

@telegram_client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    """Обработчик новых сообщений в Telegram"""
    logger.info("New message received")
    await upload_to_vk(event.message)

if __name__ == "__main__":
    logger.info("Bot started")
    telegram_client.run_until_disconnected()