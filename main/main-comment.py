# Импортируем необходимые библиотеки
import logging
import os
import random
import asyncio
from typing import List
from requests.exceptions import ConnectionError

from aiogram import Bot, Dispatcher, F, types
from background import keep_alive
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram_media_group import MediaGroupFilter, media_group_handler
from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from PIL import Image, UnidentifiedImageError
from rlottie_python import LottieAnimation
from moviepy.editor import VideoFileClip

# Загружаем переменные окружения
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Загружаем токены и идентификаторы из .env файла
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
TELEGRAM_CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME')
VK_API_TOKEN = os.getenv('VK_API_TOKEN')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')

# Инициализация сессии VK API
vk_session = VkApi(token=VK_API_TOKEN)
vk = vk_session.get_api()
uploader = VkUpload(vk)

# Инициализация бота Telegram и хранилища
bot = Bot(token=TELEGRAM_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Функция для записи ID сообщения и поста VK в файл
def add_entry(message_id, post_id):
    with open('data.txt', 'a') as f:
        f.write(f'{message_id}:{post_id}\n')

# Функция для получения ID поста VK по ID сообщения Telegram
def get_entry(message_id) -> int:
    with open('data.txt', 'r') as f:
        for line in f.readlines():
            if int(line.split(':')[0]) == message_id:
                return int(line.split(':')[1])
        raise KeyError(f'{message_id} is not in the file!')

# Создание поста в VK с вложениями
def create_vk_post(text: str, message_id, photo_list=None, video_list=None, doc_list=None, audio_list=None, gif_list=None):
    # Подготавливаем списки вложений
    photos, videos, docs, audios, gifs = [], [], [], [], []

    try:
        # Загрузка фотографий
        if photo_list:
            photos = uploader.photo_wall(photos=photo_list, group_id=VK_GROUP_ID)
        # Загрузка видео
        if video_list:
            videos = [uploader.video(video_file=path, group_id=int(VK_GROUP_ID)) for path in video_list]
        # Загрузка документов
        if doc_list:
            for doc in doc_list:
                if os.path.exists(doc):
                    with open(doc, 'rb') as f:
                        doc_info = uploader.document(doc=f, title=os.path.basename(doc))
                        docs.append(doc_info)
        # Загрузка аудио
        if audio_list:
            for audio in audio_list:
                if os.path.exists(audio):
                    with open(audio, 'rb') as f:
                        audio_info = uploader.audio(audio=f, artist="Unknown Artist", title=os.path.basename(audio))
                        audios.append(audio_info)
        # Загрузка GIF
        if gif_list:
            for gif in gif_list:
                if os.path.exists(gif):
                    with open(gif, 'rb') as f:
                        gif_info = uploader.document(doc=f, title=os.path.basename(gif))
                        gifs.append(gif_info)

        # Формирование списка вложений для VK
        attachments = [f'photo{photo.get("owner_id")}_{photo["id"]}' for photo in photos if "owner_id" in photo and "id" in photo]
        attachments += [f'video{video["owner_id"]}_{video["video_id"]}' for video in videos if "owner_id" in video and "video_id" in video]
        attachments += [f'doc{doc["doc"]["owner_id"]}_{doc["doc"]["id"]}' for doc in docs if "doc" in doc and "owner_id" in doc["doc"] and "id" in doc["doc"]]
        attachments += [f'audio{audio["owner_id"]}_{audio["id"]}' for audio in audios if "owner_id" in audio and "id" in audio]
        attachments += [f'doc{gif["doc"]["owner_id"]}_{gif["doc"]["id"]}' for gif in gifs if "doc" in gif and "owner_id" in gif["doc"] and "id" in gif["doc"]]

        # Формируем текст поста и источник
        source_link = f'https://t.me/{TELEGRAM_CHANNEL_USERNAME}/{message_id}'
        post_text = f'{text}\n\nИсточник: {source_link}'

        # Создаем пост в VK
        response = vk.wall.post(
            owner_id=f'-{VK_GROUP_ID}',
            message=post_text,
            attachments=','.join(attachments),
            from_group=1,
            copyright=source_link,
            random_id=get_random_id()
        )
        # Сохраняем ID поста
        post_id = response['post_id']
        add_entry(message_id, post_id)

    except Exception as e:
        logging.error(f'Error while creating VK post: {e}')