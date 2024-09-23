from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import *
from . import settings


@receiver(post_save, sender=TelegramUser)
def create_related_objects(sender, instance, created, **kwargs):
    if created:
        # 1. UserCoin yaratiladi
        user_coin = UserCoin.objects.create(user=instance, coin=0, limit=500, max_coin=500, add=1)

        # 3. Friend yaratiladi
        Friend.objects.create(user=user_coin, link=f"https://t.me/{settings.TELEGRAM_BOT_URL}/?start=f{instance.tg_id}")

        # 4. DailyBonus yaratiladi
        DailyBonus.objects.create(user=user_coin, limit=3)
        BoostTap.objects.create(user=user_coin, limit=3)

        # 5. Boost modellari yaratiladi
        Multitap.objects.create(user=user_coin, level=1, get_coin=5000, multitap=1)
        EnergyLimit.objects.create(user=user_coin, level=1, get_coin=5000, energy_limit=500)
        RechargingSpeed.objects.create(user=user_coin, level=1, get_coin=5000, recharging_speed=0.1)

        tasks = Task.objects.filter(outtime__gt=timezone.now())
        if tasks:
            for task in tasks:
                UserTasks.objects.create(user=user_coin, task=task)


        print(f"Related objects for {instance.full_name} have been created.")



@receiver(post_save, sender=Task)
def assign_task_to_all_users(sender, instance, created, **kwargs):
    if created:
        user_coins = UserCoin.objects.all()
        for user_coin in user_coins:
            UserTasks.objects.create(user=user_coin, task=instance)

