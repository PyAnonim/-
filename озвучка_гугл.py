import telebot
from gtts import gTTS
import os
import time
import re

from telebot.types import Message
from telebot import TeleBot, types

TOKEN = '7257116435:AAGHyYO20XdiLWPykSW48zXxrDDM12I6_kg'  # Замените на свой токен
bot = telebot.TeleBot(TOKEN)
forbidden_words = ["мат1", "мат2", "мат3", "мат4", "мат5", "мат6","мат7 и тд..."]

@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.reply_to(message, "Теперь отправляй текст для озвучки 💬")
@bot.message_handler(content_types=['sticker', 'audio' , 'video' , 'voice' , 'photo' , 'document' , 'location' , 'contact'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("✅ Скрыть ✅", callback_data="delete_chat"))
    bot.send_message(message.chat.id, "Этот тип данных не поддерживается 🚫", reply_markup=markup)
    @bot.callback_query_handler(func=lambda call: call.data == "delete_chat")
    def handle_delete_chat(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)

    @bot.callback_query_handler(func=lambda call: call.data == "close")
    def handle_close_chat(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)

    @bot.callback_query_handler(func=lambda call: call.data == "close")
    def handle_close_chat(call):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(message.chat.id, message.message_id)
@bot.message_handler(content_types=['text'])
def parse_message(message):
    
    # Извлечение текста для озвучивания
    text_to_speak = message.text
    
    bot.send_chat_action(message.chat.id, 'record_voice')
    # Создание голосового сообщения с помощью gTTS
    tts = gTTS(text=text_to_speak, lang='ru')
    audio_file = "ㅤ"
    tts.save(audio_file)

    bot.send_chat_action(message.chat.id, 'upload_audio')


    bot.reply_to(message, "✅")
    with open(audio_file, "rb") as speech_file:
        bot.send_voice(message.chat.id, speech_file)


    # Удаляем временный файл
    os.remove(audio_file)


# Запуск бота
bot.polling(none_stop=True)