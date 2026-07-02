
import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading

# إعدادات البوت
TOKEN = '8977849022:AAHwThIrcSeYsvZsemuo2l5sFnb7p898Mow'
CHAT_ID = '1718292210'
bot = telebot.TeleBot(TOKEN)

def check_news():
    while True:
        try:
            url = "https://www.forexfactory.com/calendar"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # العثور على جدول الأخبار
            table = soup.find('table', class_='calendar__table')
            if table:
                rows = table.find_all('tr', class_='calendar__row')
                news_text = "📊 *تحديث السوق القادم:* \n\n"
                count = 0
                
                # استخراج حتى 6 أخبار
                for row in rows:
                    if count >= 6: break
                    
                    time_el = row.find('td', class_='calendar__time')
                    event_el = row.find('td', class_='calendar__event')
                    currency_el = row.find('td', class_='calendar__currency')
                    
                    if time_el and event_el and currency_el:
                        news_text += f"🕒 {time_el.text.strip()} | {currency_el.text.strip()} | {event_el.text.strip()}\n"
                        count += 1
                
                if count > 0:
                    bot.send_message(CHAT_ID, news_text, parse_mode="Markdown")
            
        except Exception as e:
            print(f"حدث خطأ: {e}")
            
        # الانتظار لمدة 10 دقائق (600 ثانية) قبل الفحص القادم
        time.sleep(600)

# بدء التشغيل
threading.Thread(target=check_news, daemon=True).start()
print("البوت يعمل الآن.. وسيقوم بالتحديث كل 10 دقائق")
bot.send_message(CHAT_ID, "✅ البوت يعمل الآن وبدأ في مراقبة الأخبار..")
bot.infinity_polling()

