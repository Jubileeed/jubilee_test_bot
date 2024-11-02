import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont

# Инициализация бота
bot = telebot.TeleBot('7081132142:AAGhU15Nae1QsBVsRO18XX5xvYkJUHUeRVg')  # Замените 'YOUR_BOT_TOKEN' на ваш токен

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот-генератор мемов. Для начала работы отправь картинку - основу мема.')

# Обработчик сообщений с фотографиями
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'Фото успешно сохранено!\nТеперь напишите текст, который вы хотите добавить на фото.')
    bot.register_next_step_handler(message, set_photo_text)

# Обработчик текста для мема
def set_photo_text(message):
    try:
        image = Image.open('photo.jpg')
        draw = ImageDraw.Draw(image)
        # Загрузка шрифта, поддерживающего кириллицу
        font = ImageFont.truetype("arial.ttf", 60)  # Убедитесь, что файл находится в рабочем каталоге
        text = message.text

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image.width - text_width) / 2
        y = image.height - text_height - 20


        draw.text((x, y), text.upper(), font=font, fill=(0, 0, 0))
        image.save('photo_mem.jpg')

        with open('photo_mem.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при обработке изображения. Попробуйте еще раз.')
        print(e)

# Запуск бота
bot.polling(none_stop=True)
