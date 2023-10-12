import sqlite3
import psycopg2
from psycopg2.extras import NamedTupleCursor

from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sys

import settings
app = Flask(__name__)

TOKEN = "6199157737:AAHHlXFQ2vsXTuLeQ_rBtISoi72qja3EdK0"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    print(update.message.from_user, file=sys.stderr)
    user_data=update.message.from_user
    conn = psycopg2.connect(dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD, host='127.0.0.1')

    cur = conn.cursor()
    get_query = "SELECT * FROM user_user WHERE telega LIKE (%s)"
    cur.execute(get_query, (user_data.username,))
    user = cur.fetchone()
    print(user)
    print(user[13])

    if user:

        if not user[13]:
            update.message.reply_text("ID успешно установлен")
            print('save')
            update_query = "UPDATE user_user SET telega_id=(%s) WHERE id=(%s)"
            cur.execute(update_query, (user_data.id, user[0],))
            conn.commit()
            cur.close()
        else:
            update.message.reply_text("Привет! ")
    else:
        update.message.reply_text("Привет! Твой телеграм username не найден в базе")



def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Вы написали: {update.message.text}")


@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.json
    chat_id = content['chat_id']
    message = content['message']
    updater.bot.send_message(chat_id=chat_id, text=message)

    return jsonify({'status': 'ok'})


def main():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
