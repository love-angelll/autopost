<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

# Бот для автоматической публикации сообщений из Telegram в ВКонтакте

Этот проект представляет собой скрипт на Python, который автоматически публикует сообщения из Telegram-канала или чата в указанную группу ВКонтакте. Он поддерживает различные типы контента, включая текст, изображения, видео и ссылки.

## Структура проекта

```
main
├── main
│   ├── files             # Папка где временно сохраняется фото, видео. Потом сами удаляются.
│   ├── main.py           # Основная логика для скрипта автоматической публикации
│   ├── settings.toml       # Конфигурационный файл для учетных данных API
│   ├── logs.log          # Логи скрипта
│   └── helpers.py          # Служебные функции для анализа и форматирования сообщений
├── requirements.txt      # Необходимые библиотеки для проекта
└── README.md             # Документация по проекту
```

3. **Настройте бота:** <br>
 Отредактируйте файл `main/settings.toml`, чтобы в нем были указаны ваши учетные данные для Telegram и ВКонтакте API:<br>
 ```toml
[telegram]
api_id = "26831388"
api_hash = "43ad46e4d53c5ff1ca0e27c9ca4407b7"
bot_token = "7458801028:AAF2Ze8Ukd1faOI3SGo4nGFzKk6dOGyf9uE"
channel_id = 1001927626277

[vk]
token = "vk1.a.BujFws4sioTB7zJ3p5i40Aq9IVWhnnU910z1OCd2teuGXv4ZH2XrA8S-Tlab14XAWRl_OpmMuxHs4sG8-YE-xfWI9NDCE_uMBwFLQHP4njlLAJa8dKuldBPDIoG4GCs2__PEIi165kON4uni8_LB0rxfpC7RAGm4icDXQqrBrZIwkV8fGu1-Dh2V1sdNnVofVYQ_VOwK8rTbAXHkChA8tQ"
user_token = "vk1.a.bgWN2zuvjShCqKD326a2CxmF5_jj_jVaePV7d3upl5Yczwru_8tVeQ89DWOKn9nVMozHRAm8ZjZY-R9nppKNxa4tVgPlAIegXy-P1730fzxjwAzHnXGDBVRBIXhDUd2KxfUiDF_LSLMTag6ChUrTe-BVNpk4GLbeYSejkJxjJIczkgH8qajImhwgTyaFGoNxs2RC_Bh4sXddOc9B8J0HeQ"
group_id = "29899402"
 ```

## Особенности

- Поддерживает публикацию текстовых сообщений, изображений, видео и ссылок.
- Настраивается с помощью простого файла TOML.
- Регистрирует активность, что помогает в отладке и мониторинге.

## Содействие

Не стесняйтесь отправлять проблемы или запросы на исправление, если у вас есть какие-либо вопросы то пишите в соц. сетях.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/iv_frunza)
[![VK Основной](https://img.shields.io/badge/VK%20Основной-4A76A8?style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/iv.frunza)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/iv.frunza)
