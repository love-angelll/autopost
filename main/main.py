import logging
import os
import random
import asyncio
from typing import List
from requests.exceptions import ConnectionError

from aiogram import Bot, Dispatcher, F, types
# from background import keep_alive
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram_media_group import MediaGroupFilter, media_group_handler
from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from PIL import Image, UnidentifiedImageError
from rlottie_python import LottieAnimation
from moviepy import VideoFileClip

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
TELEGRAM_CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME')
VK_API_TOKEN = os.getenv('VK_API_TOKEN')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')

vk_session = VkApi(token=VK_API_TOKEN)
vk = vk_session.get_api()
uploader = VkUpload(vk)
bot = Bot(token=TELEGRAM_API_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)

def add_entry(message_id, post_id):
    with open('data.txt', 'a') as f:
        f.write(f'{message_id}:{post_id}\n')


def get_entry(message_id) -> int:
    with open('data.txt', 'r') as f:
        for line in f.readlines():
            if int(line.split(':')[0]) == message_id:
                return int(line.split(':')[1])
        raise KeyError(f'{message_id} is not in the file!')


def create_vk_post(text: str, message_id, photo_list=None, video_list=None, doc_list=None, audio_list=None, gif_list=None):
    photos, videos, docs, audios, gifs = [], [], [], [], []

    try:
        if photo_list:
            photos = uploader.photo_wall(photos=photo_list, group_id=VK_GROUP_ID)
        if video_list:
            videos = [uploader.video(video_file=path, group_id=int(VK_GROUP_ID)) for path in video_list]
        if doc_list:
            for doc in doc_list:
                if os.path.exists(doc):
                    with open(doc, 'rb') as f:
                        doc_info = uploader.document(doc=f, title=os.path.basename(doc))
                        docs.append(doc_info)
        if audio_list:
            for audio in audio_list:
                if os.path.exists(audio):
                    with open(audio, 'rb') as f:
                        audio_info = uploader.audio(audio=f, artist="Unknown Artist", title=os.path.basename(audio))
                        audios.append(audio_info)
        if gif_list:
            for gif in gif_list:
                if os.path.exists(gif):
                    with open(gif, 'rb') as f:
                        gif_info = uploader.document(doc=f, title=os.path.basename(gif))
                        gifs.append(gif_info)

        attachments = [f'photo{photo.get("owner_id")}_{photo["id"]}' for photo in photos if "owner_id" in photo and "id" in photo]
        attachments += [f'video{video["owner_id"]}_{video["video_id"]}' for video in videos if "owner_id" in video and "video_id" in video]
        attachments += [f'doc{doc["doc"]["owner_id"]}_{doc["doc"]["id"]}' for doc in docs if "doc" in doc and "owner_id" in doc["doc"] and "id" in doc["doc"]]
        attachments += [f'audio{audio["owner_id"]}_{audio["id"]}' for audio in audios if "owner_id" in audio and "id" in audio]
        attachments += [f'doc{gif["doc"]["owner_id"]}_{gif["doc"]["id"]}' for gif in gifs if "doc" in gif and "owner_id" in gif["doc"] and "id" in gif["doc"]]

        source_link = f'https://t.me/{TELEGRAM_CHANNEL_USERNAME}/{message_id}'
        post_text = f'{text}\n\nИсточник: {source_link}'

        response = vk.wall.post(
            owner_id=f'-{VK_GROUP_ID}',
            message=post_text,
            attachments=','.join(attachments),
            from_group=1,
            copyright=source_link,
            random_id=get_random_id()
        )
        post_id = response['post_id']
        add_entry(message_id, post_id)

    except Exception as e:
        logging.error(f'Error while creating VK post: {e}')


def edit_vk_post(post_id, new_text, message_id):
    old_post = vk.wall.getById(posts=f'-{VK_GROUP_ID}_{post_id}')[0]
    attachments = [f'{attachment["type"]}{attachment[attachment["type"]]["owner_id"]}_{attachment[attachment["type"]]["id"]}' for attachment in old_post.get('attachments', [])]

    source_link = f'https://t.me/{TELEGRAM_CHANNEL_USERNAME}/{message_id}'
    edited_text = f'{new_text}\n\nИсточник: {source_link}'

    vk.wall.edit(
        message=edited_text,
        post_id=post_id,
        from_group=1,
        owner_id=f'-{VK_GROUP_ID}',
        copyright=source_link,
        attachments=attachments
    )


async def download_file_with_retries(file_id: str, destination: str, retries: int = 3, delay: int = 5):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    for attempt in range(retries):
        try:
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, destination)
            return True
        except Exception as e:
            logging.error(f'Error while downloading file (attempt {attempt + 1}/{retries}): {e}')
            if attempt < retries - 1:
                await asyncio.sleep(delay)
    return False


@media_group_handler
async def album_handler(messages: List[Message]):
    random_number = random.randint(1000000, 9999999)
    c = 0

    photo_list = []
    video_list = []
    doc_list = []
    audio_list = []
    gif_list = []
    text = None

    for message in messages:
        if message.caption and not text:
            text = message.caption
        if message.photo:
            path = f'./files/photo_{random_number}_{c}.jpg'
            if await download_file_with_retries(message.photo[-1].file_id, path):
                photo_list.append(path)
        elif message.video:
            path = f'./files/video_{random_number}_{c}.mp4'
            if await download_file_with_retries(message.video.file_id, path):
                video_list.append(path)
        elif message.document:
            path = f'./files/doc_{random_number}_{c}_{message.document.file_name}'
            if await download_file_with_retries(message.document.file_id, path):
                doc_list.append(path)
        elif message.audio:
            path = f'./files/audio_{random_number}_{c}_{message.audio.file_name}'
            if await download_file_with_retries(message.audio.file_id, path):
                audio_list.append(path)
        elif message.animation:
            path = f'./files/gif_{random_number}_{c}.mp4'
            if await download_file_with_retries(message.animation.file_id, path):
                gif_list.append(path)
        c += 1

    message_id = messages[0].message_id
    post_text = text if text else ''
    await asyncio.to_thread(create_vk_post, post_text, message_id, photo_list, video_list, doc_list, audio_list, gif_list)
    
    for path in photo_list + video_list + doc_list + audio_list + gif_list:
        os.remove(path)


async def photo_video_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    if message.photo:
        path = f'./files/photo_{random_number}.jpg'
        if await download_file_with_retries(message.photo[-1].file_id, path):
            await asyncio.to_thread(create_vk_post, text, message.message_id, [path])
            os.remove(path)
    elif message.video:
        path = f'./files/video_{random_number}.mp4'
        if await download_file_with_retries(message.video.file_id, path):
            await asyncio.to_thread(create_vk_post, text, message.message_id, None, [path])
            os.remove(path)


async def document_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    path = f'./files/doc_{random_number}_{message.document.file_name}'
    if await download_file_with_retries(message.document.file_id, path):
        await asyncio.to_thread(create_vk_post, text, message.message_id, None, None, [path])
        os.remove(path)


async def audio_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    audio_paths = []
    for i, audio in enumerate(message.audio):
        path = f'./files/audio_{random_number}_{i}_{audio.file_name}'
        if await download_file_with_retries(audio.file_id, path):
            if os.path.exists(path):
                audio_paths.append(path)
    if audio_paths:
        await asyncio.to_thread(create_vk_post, text, message.message_id, None, None, None, audio_paths)
        for path in audio_paths:
            os.remove(path)


async def video_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    path = f'./files/video_{random_number}_{message.video.file_name}'
    if await download_file_with_retries(message.video.file_id, path):
        if os.path.exists(path):
            await asyncio.to_thread(create_vk_post, text, message.message_id, None, [path])
            os.remove(path)


async def text_handler(message: Message):
    await asyncio.to_thread(create_vk_post, message.text, message.message_id)


async def edited_handler(message: Message):
    if message.message_id is None:
        return

    try:
        post_id = get_entry(message.message_id)
    except KeyError:
        return

    text = message.text or message.caption or ''
    await asyncio.to_thread(edit_vk_post, post_id, text, message.message_id)


async def sticker_handler(message: Message):
    random_number = random.randint(1000000, 9999999)
    path = f'./files/sticker_{random_number}.{"tgs" if message.sticker.is_animated else "webp"}'
    if await download_file_with_retries(message.sticker.file_id, path):
        if message.sticker.is_animated or message.sticker.is_video:
            try:
                gif_path = f'./files/sticker_{random_number}.gif'

                if message.sticker.is_animated:
                    animation = LottieAnimation.from_tgs(path)
                    frames = [animation.render_pillow_frame(frame_num=i) for i in range(animation.lottie_animation_get_totalframe())]
                    frames[0].save(gif_path, save_all=True, append_images=frames[1:], loop=0, duration=1000 // animation.lottie_animation_get_framerate())
                else:
                    clip = VideoFileClip(path)
                    clip.write_gif(gif_path)
                    clip.close()

                os.remove(path)
                await asyncio.to_thread(create_vk_post, '', message.message_id, None, None, None, None, [gif_path])
                os.remove(gif_path)
            except Exception as e:
                logging.error(f'Error while converting animated sticker: {e}')
                try:
                    os.remove(path)
                except PermissionError:
                    pass
        else:
            try:
                png_path = f'./files/sticker_{random_number}.png'
                try:
                    with Image.open(path) as im:
                        width, height = im.size
                        scale = 1.0
                        width_new, height_new = int(width * scale), int(height * scale)
                        im_resized = im.resize((width_new, height_new), Image.LANCZOS)
                        im_resized.save(png_path, 'PNG')
                except UnidentifiedImageError as e:
                    raise
                os.remove(path)
                await asyncio.to_thread(create_vk_post, '', message.message_id, [png_path], None, None, None, None)
                os.remove(png_path)
            except Exception as e:
                logging.error(f'Error while converting static sticker: {e}')
                if os.path.exists(path):
                    os.remove(path)


async def voice_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    path = f'./files/voice_{random_number}.ogg'

    download_task = asyncio.create_task(download_file_with_retries(message.voice.file_id, path, retries=5, delay=10))

    try:
        await download_task
        if not os.path.exists(path):
            return
    except Exception as e:
        return

    file_size = os.path.getsize(path)
    max_size = 10 * 1024 * 1024
    if file_size > max_size:
        os.remove(path)
        return

    await asyncio.to_thread(create_vk_post, text, message.message_id, None, None, None, [path])
    os.remove(path)


async def animation_handler(message: Message):
    text = message.caption or ''
    random_number = random.randint(1000000, 9999999)
    path = f'./files/animation_{random_number}.mp4'
    retries = 3
    delay = 5
    for attempt in range(retries):
        try:
            if await download_file_with_retries(message.animation.file_id, path):
                gif_path = f'./files/animation_{random_number}.gif'
                clip = VideoFileClip(path)
                clip.write_gif(gif_path)
                clip.close()
                os.remove(path)
                await asyncio.to_thread(create_vk_post, text, message.message_id, None, None, None, None, [gif_path])
                os.remove(gif_path)
                break
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                logging.error(f'Failed to download animation {message.animation.file_id} after {retries} attempts')

async def main():
    dp.channel_post.register(album_handler, MediaGroupFilter())
    dp.channel_post.register(photo_video_handler, F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO]))
    dp.channel_post.register(document_handler, F.content_type == ContentType.DOCUMENT)
    dp.channel_post.register(audio_handler, F.content_type == ContentType.AUDIO)
    dp.channel_post.register(video_handler, F.content_type == ContentType.VIDEO)
    dp.channel_post.register(text_handler, F.content_type == ContentType.TEXT)
    dp.channel_post.register(sticker_handler, F.content_type == ContentType.STICKER)
    dp.channel_post.register(animation_handler, F.content_type == ContentType.ANIMATION)
    dp.channel_post.register(voice_handler, F.content_type == ContentType.VOICE)
    dp.edited_channel_post.register(edited_handler)

    await dp.start_polling(bot)
    
if __name__ == '__main__':
    logging.info('Starting bot')
    asyncio.run(main())
