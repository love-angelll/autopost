import asyncio
import logging
import os
import shutil
import toml

from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage
import vk_api
import requests

from utils import format_message_for_vk

# Настройка логирования
logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.info("Запуск скрипта")

# Загрузка конфигурации
config_path = os.path.join(os.path.dirname(__file__), 'settings.toml')
try:
    config = toml.load(config_path)
    logging.info("Конфигурационный файл успешно загружен")
except Exception as e:
    logging.error(f"Ошибка при загрузке конфигурационного файла: {e}")
    raise

VK_TOKEN = config["vk"]["token"]
GROUP_ID = config["vk"]["group_id"]

telegram_api_id = config["telegram"]["api_id"]
telegram_api_hash = config["telegram"]["api_hash"]
telegram_bot_token = config["telegram"]["bot_token"]
telegram_channel_id = int(config["telegram"]["channel_id"])

vk_user_token = config["vk"]["user_token"]

# Инициализация Telegram клиента
try:
    telegram_client = TelegramClient("telegram_bot", telegram_api_id, telegram_api_hash)
    logging.info("Telegram клиент инициализирован")
except Exception as e:
    logging.error(f"Ошибка при инициализации Telegram клиента: {e}")
    raise

# Инициализация VK API клиента для группы
try:
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    logging.info("VK API клиент инициализирован")
except Exception as e:
    logging.error(f"Ошибка при инициализации VK API клиента: {e}")
    raise

# Инициализация VK API клиента для пользователя
try:
    vk_user_session = vk_api.VkApi(token=vk_user_token)
    vk_user = vk_user_session.get_api()
    logging.info("VK API клиент для пользователя инициализирован")
except Exception as e:
    logging.error(f"Ошибка при инициализации VK API клиента для пользователя: {e}")
    raise

# Создание папки files, если она не существует
files_dir = 'files'
if not os.path.exists(files_dir):
    os.makedirs(files_dir)

def upload_photo_to_vk(photo_path):
    upload_url = vk_user.photos.getWallUploadServer(group_id=GROUP_ID)['upload_url']
    with open(photo_path, 'rb') as photo_file:
        response = requests.post(upload_url, files={'photo': photo_file}).json()
    photo = vk_user.photos.saveWallPhoto(group_id=GROUP_ID, photo=response['photo'], server=response['server'], hash=response['hash'])[0]
    return f"photo{photo['owner_id']}_{photo['id']}"

def upload_document_to_vk(doc_path, title):
    upload_url = vk_user.docs.getWallUploadServer(group_id=GROUP_ID)['upload_url']
    with open(doc_path, 'rb') as doc_file:
        response = requests.post(upload_url, files={'file': doc_file}).json()
    doc = vk_user.docs.save(file=response['file'], title=title)[0]
    return f"doc{doc['owner_id']}_{doc['id']}"

def upload_video_to_vk(video_path, name):
    save_response = vk_user.video.save(name=name, group_id=GROUP_ID, is_private=0)
    upload_url = save_response['upload_url']
    with open(video_path, 'rb') as video_file:
        response = requests.post(upload_url, files={'video_file': video_file}).json()
    return f"video{save_response['owner_id']}_{save_response['video_id']}"

def split_message(text, max_length=4096):
    """Разбить сообщение на части, если оно превышает максимальную длину"""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@telegram_client.on(events.NewMessage(chats=telegram_channel_id))
async def handler(event):
    try:
        message = event.message
        logging.info(f"Получено сообщение из Telegram: {message.text if message.text else 'не текстовое сообщение'}")

        # Обработка медиа-контента
        attachments = []
        if message.grouped_id:
            # Получаем все сообщения из медиа-группы
            media_list = await telegram_client.get_messages(event.chat_id, ids=range(message.id - 9, message.id + 1))
            for media in media_list:
                if media.grouped_id != message.grouped_id:
                    continue
                if isinstance(media.media, MessageMediaPhoto):
                    logging.info("Обработка фотографии")
                    # Загрузка фотографии
                    photo_path = await media.download_media(file=files_dir)
                    attachments.append(upload_photo_to_vk(photo_path))
                    os.remove(photo_path)

                elif isinstance(media.media, MessageMediaDocument):
                    if "video" in media.file.mime_type:
                        logging.info("Обработка видео")
                        # Загрузка видео
                        video_path = await media.download_media(file=files_dir)
                        attachments.append(upload_video_to_vk(video_path, media.file.name))
                        os.remove(video_path)
                    else:
                        logging.info("Обработка документа")
                        # Загрузка документа
                        doc_path = await media.download_media(file=files_dir)
                        attachments.append(upload_document_to_vk(doc_path, media.file.name))
                        os.remove(doc_path)

                elif isinstance(media.media, MessageMediaWebPage):
                    logging.info("Обработка веб-страницы")
                    # Обработка ссылок
                    formatted_message = format_message_for_vk(media)
                    vk.wall.post(owner_id=-int(GROUP_ID), message=formatted_message)
                    return

                else:
                    logging.warning("Неизвестный тип медиа")

        if not attachments and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                logging.info("Обработка фотографии")
                # Загрузка фотографии
                photo_path = await message.download_media(file=files_dir)
                attachments.append(upload_photo_to_vk(photo_path))
                os.remove(photo_path)

            elif isinstance(message.media, MessageMediaDocument):
                if "video" in message.file.mime_type:
                    logging.info("Обработка видео")
                    # Загрузка видео
                    video_path = await message.download_media(file=files_dir)
                    attachments.append(upload_video_to_vk(video_path, message.file.name))
                    os.remove(video_path)
                else:
                    logging.info("Обработка документа")
                    # Загрузка документа
                    doc_path = await message.download_media(file=files_dir)
                    attachments.append(upload_document_to_vk(doc_path, message.file.name))
                    os.remove(doc_path)

            elif isinstance(message.media, MessageMediaWebPage):
                logging.info("Обработка веб-страницы")
                # Обработка ссылок
                formatted_message = format_message_for_vk(message)
                vk.wall.post(owner_id=-int(GROUP_ID), message=formatted_message)
                return

            else:
                logging.warning("Неизвестный тип медиа")

        # Отправка текстового сообщения с сохранением форматирования
        formatted_message = format_message_for_vk(message)
        for part in split_message(formatted_message):
            vk.wall.post(owner_id=-int(GROUP_ID), message=part, attachments=','.join(attachments))
        logging.info(f"Сообщение опубликовано в VK: {formatted_message}")

    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

async def main():
    try:
        await telegram_client.start(bot_token=telegram_bot_token)
        logging.info("Telegram клиент запущен")
        await telegram_client.run_until_disconnected()
    except Exception as e:
        logging.error(f"Ошибка в главной функции: {e}")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        logging.error(f"Ошибка при запуске событийного цикла: {e}")
