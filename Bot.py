import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

def get_price(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price_tag = soup.find('td', class_='nf')
        return price_tag.text.strip()
    except:
        return "نامشخص"

def get_all_prices():
    prices = {
        'دلار': get_price('https://www.tgju.org/profile/price_dollar_rl'),
        'یورو': get_price('https://www.tgju.org/profile/price_eur'),
        'طلای 18 عیار': get_price('https://www.tgju.org/profile/geram18'),
    }
    return prices

def format_message(prices):
    message = "📊 <b>قیمت‌های لحظه‌ای بازار</b>:\n\n"
    for name, value in prices.items():
        message += f"🔸 <b>{name}</b>: {value} تومان\\n"
    message += "\\n⏱ بروزرسانی خودکار هر ۲ دقیقه"
    return message

def send_to_channel(text):
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='HTML')

if __name__ == '__main__':
    while True:
        try:
            prices = get_all_prices()
            message = format_message(prices)
            send_to_channel(message)
            print("✅ ارسال موفق")
        except Exception as e:
            print(f'❌ خطا: {e}')
        time.sleep(120)  # هر ۲ دقیقه
