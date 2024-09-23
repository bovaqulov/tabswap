import telebot
from django.conf import settings
from telebot.apihelper import ApiTelegramException
import schedule
import time
import threading
from django.db import models
from .models import UserCoin, RechargingSpeed


bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

def check_member(chat_id, user_id):
    link = '@'+ chat_id.split('/')[-1] if not "@" in chat_id else chat_id
    try:
        member = bot.get_chat_member(link, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except ApiTelegramException:
        return False

def add_coins():
    users = UserCoin.objects.filter(max_coin__lt=models.F('limit'))

    for user in users:
        recharging_speed = RechargingSpeed.objects.get(user=user)


        if user.max_coin - user.limit < (user.add * recharging_speed.recharging_speed):
            user.max_coin = user.limit
            user.save()

        if user.max_coin < user.limit:
            user.max_coin += (user.add * recharging_speed.recharging_speed)
            user.save()

schedule.every(0.1).minutes.do(add_coins)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler_in_thread():
    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()
