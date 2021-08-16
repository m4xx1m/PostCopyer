from aiogram import Bot, Dispatcher, executor, types
import json
from time import sleep
import asyncio
import schedule
import datetime
import logging

file_log = logging.FileHandler('log.txt')
console_out = logging.StreamHandler()
logging.basicConfig(
    handlers=(file_log, console_out),
    format='[%(levelname)s][%(asctime)s] %(message)s',
    level=logging.INFO,
)

loop = asyncio.get_event_loop()

config = json.load(open('config.json', 'r', encoding="UTF-8"))

bot = Bot(config['token'], loop=loop)
dp = Dispatcher(bot, loop=loop)


async def send(from_chat_id, message_id, chat_id):
    await bot.copy_message(
        from_chat_id=from_chat_id,
        chat_id=chat_id,
        message_id=message_id
    )


def send_(from_chat_id, message_id, chat_id):
    loop.run_until_complete(send(from_chat_id, message_id, chat_id))


@dp.message_handler()
async def pinger(message: types.Message):
    if message.from_user.id in config['admins']:
        start = datetime.now()
        msg = await message.reply("[оk]")
        end = datetime.now()
        duration = (end - start).microseconds / 1000
        await msg.edit(f'[оk] {str(duration)[0:5]}ms')
        logging.info(f'Ping [{str(duration)[0:5]}]')


if __name__ == '__main__':
    for chats in config['msgs'].keys():
        for time in config['msgs'][chats]['times']:
            schedule.every().day.at(time).do(send_,
                from_chat_id=config['from_chat_id'],
                message_id=config['msgs'][chats]['msg'],
                chat_id=config['msgs'][chats]['id']
            )
    while True:
        schedule.run_pending()
        sleep(1)
