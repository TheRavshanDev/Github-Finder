from aiogram import Bot, Dispatcher, executor, types
import re
import requests
from bs4 import BeautifulSoup

API_TOKEN = '1840368605:AAHImlDRtebIxvvRIky-kvO0DJ0ney7_5CU'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
urls_list = []

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("🖐Welcome to the bot that easily downloads codes from Github! \nJust type a title to 📥upload the code ")

@dp.message_handler()
async def extract_data(message: types.Message):
    await message.answer("⌛️Wanted on Github ... ")
    reg_ex = re.search('(.+)', message.text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = f'https://github.com/search?q={domain}&type='
        result_link = None
    responce = requests.get(f'{url}').text
    soup = BeautifulSoup(responce)
    block = soup.find('div', class_='position-relative js-header-wrapper ')
    all_topics = soup.find_all('div',class_="f4 text-normal")

    for topic in all_topics:
        topic_link = topic.find('a').get('href')
        print(topic_link)
        url = f'https://github.com/{topic_link}'
        download_storage = requests.get(f'{url}').text
        soup = BeautifulSoup(download_storage)
        kod = soup.find_all('div',target_='get-repo.modal')
        code = kod.find('a',class_='d-flex flex-items-center color-fg-default text-bold no-underline').get('href')
        print(code)
        await message.answer(f'✅The code was loaded successfully  \n\nhttps://github.com/{code}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)