import telebot
# 参考文档：https://github.com/eternnoir/pyTelegramBotAPI
bot = telebot.TeleBot("6499352151:AAFmCL36N8tpynKi45pghC7R567fRFfQE9M", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "你好, 你可以输入 /start 或者 /help")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()

if __name__ == '__main__':
    pass
