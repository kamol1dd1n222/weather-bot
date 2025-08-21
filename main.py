from telegram.ext import (
    Updater,CommandHandler,MessageHandler,Filters,CallbackContext
)
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton
from config import TOKEN, API_TOKEN
import requests


 
def start(update:Update,contex:CallbackContext):
    keyboard = [
        [KeyboardButton(' 📍Lokatsiyani yuborish', request_location=True)]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    user_name = update.effective_user
    update.message.reply_text(f"Salom {user_name.first_name}, Locatsiyani yuborish uchun tugmani bosing 👇",
                reply_markup=reply_markup)
    

def location_weather(update:Update,contex:CallbackContext):
    user_location = update.message.location
    
    if  not user_location:
        return
    url = "http://api.weatherapi.com/v1/current.json"
    latitute = user_location.latitude
    longtitute = user_location.longitude
    params = {
        'key':API_TOKEN,
        'q':f"{latitute},{longtitute}",
        'lang':'uz'
    }
    response = requests.get(url,params=params).json()
    print(response)
    
    try:
        if "error" in response:
            update.message.reply_text("❌ API xatolik qaytardi.")
            return
        city = response["location"]["name"]
        country = response["location"]["country"]
        temp_c = response["current"]["temp_c"]
        condition = response["current"]["condition"]["text"]

        update.message.reply_text(
            f"📍 Joy: {city}, {country}\n"
            f"🌡 Harorat: {temp_c}°C\n"
            f"🌅 Holat: {condition}"
        )

    
    except (ValueError, KeyError) as e:
        update.message.reply_text("❌ Ob-havo ma'lumotini olishda xatolik yuz berdi.")
        
        
def main() -> None:
     updater  = Updater(TOKEN)
     dispatcher = updater.dispatcher
     
     dispatcher.add_handler(CommandHandler('start',start))
     dispatcher.add_handler(MessageHandler(Filters.location,location_weather))
     
     updater.start_polling()
     updater.idle()
     
main()
     