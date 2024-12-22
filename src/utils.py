import re

def format_message_for_vk(message):
    # Пример простой функции форматирования сообщений
    if message.text:
        return message.text
    elif message.media:
        # Обработка медиа (изображения, видео и т.д.)
        return "Медиа сообщение"
    else:
        return "Неизвестный тип сообщения"