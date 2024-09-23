from django.db import models

# TelegramUser Model
class TelegramUser(models.Model):
    tg_id = models.BigIntegerField(unique=True)  # Katta qiymatlarni ham saqlash uchun BigIntegerField
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name


# UserCoin Model
class UserCoin(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, related_name='user_coin')
    coin = models.PositiveIntegerField(default=0)  # Manfiy bo'lmagan qiymatlar uchun PositiveIntegerField
    limit = models.PositiveIntegerField(default=500)
    max_coin = models.PositiveIntegerField(default=500)
    add = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user}'s Coin Data"


# InviteFriend Model
class InviteFriend(models.Model):
    user = models.OneToOneField(UserCoin, on_delete=models.CASCADE, related_name='invite_friend')
    is_done = models.BooleanField(default=False)
    coin = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return f"InviteFriend for {self.user}"


# Friend Model
class Friend(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='friends')
    link = models.URLField(max_length=500)  # link maydonini URLField bilan almashtirish
    invited_friends = models.ManyToManyField(InviteFriend, related_name='invited_by')

    def __str__(self):
        return f"Friend link for {self.user}"


# Task Model
class Task(models.Model):
    TELEGRAM = 'telegram'
    VIDEO = 'video'
    OTHERS = 'others'

    TASK_TYPES = [
        (TELEGRAM, 'Telegram'),
        (VIDEO, 'Video'),
        (OTHERS, 'Others'),
    ]

    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500)  # URLField bilan almashtirish
    coin = models.PositiveIntegerField(default=25000)
    type = models.CharField(max_length=50, choices=TASK_TYPES)
    outtime = models.DateTimeField()

    def __str__(self):
        return self.name


# Abstract Boost Model
class Boost(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='%(class)s_boosts')
    level = models.PositiveIntegerField(default=0)
    get_coin = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


# Multitap Model inheriting Boost
class Multitap(Boost):
    multitap = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Multitap Boost for {self.user}"


# EnergyLimit Model inheriting Boost
class EnergyLimit(Boost):
    energy_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Energy Limit Boost for {self.user}"


# RechargingSpeed Model inheriting Boost
class RechargingSpeed(Boost):
    recharging_speed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Recharging Speed Boost for {self.user}"


# DailyBonus Model
class DailyBonus(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='daily_bonus')
    limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Daily Bonus for {self.user}"

class BoostTap(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='boost_tap')
    limit = models.PositiveIntegerField(default=3)


    def __str__(self):
        return f"Daily Bonus for {self.user}"

# UserTasks Model
class UserTasks(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='user_tasks')
    is_complete = models.BooleanField(default=False)
    is_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task '{self.task.name}' for user '{self.user.user.full_name}'"


class Voucher(models.Model):
    name = models.CharField(max_length=255)
    coin = models.PositiveIntegerField(default=1000000)
    som = models.PositiveIntegerField(default=1000)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Voucher for {self.name}"

class Admins(models.Model):
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='admins')

    def __str__(self):
        return f"Admin for {self.user}"


class VoucherUser(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(UserCoin, on_delete=models.CASCADE, related_name='voucher_users')
    is_claimed = models.BooleanField(default=False)
    at_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VoucherUser for {self.user}"


