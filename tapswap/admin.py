# tapswap/admin.py

from django.contrib import admin
from .models import (
    TelegramUser, UserCoin, InviteFriend, Friend, Task, Multitap,
    EnergyLimit, RechargingSpeed, DailyBonus, UserTasks, BoostTap,
    Admins, Voucher, VoucherUser
)

# TelegramUser Modelini ro'yxatdan o'tkazish
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'full_name', 'username')
    search_fields = ('full_name', 'username', 'tg_id')


# UserCoin Modelini ro'yxatdan o'tkazish
@admin.register(UserCoin)
class UserCoinAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin', 'limit', 'max_coin', 'add')
    search_fields = ('user__full_name', 'user__tg_id')
    list_filter = ('max_coin', 'limit')


# InviteFriend Modelini ro'yxatdan o'tkazish
@admin.register(InviteFriend)
class InviteFriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_done', 'coin')
    list_filter = ('is_done',)


# Friend Modelini ro'yxatdan o'tkazish
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'link')
    search_fields = ('user__user__full_name', 'link')
    filter_horizontal = ('invited_friends',)


# Task Modelini ro'yxatdan o'tkazish
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'coin', 'outtime')
    search_fields = ('name', 'type')
    list_filter = ('type', 'outtime')


# Multitap Modelini ro'yxatdan o'tkazish
@admin.register(Multitap)
class MultitapAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'get_coin', 'multitap')
    list_filter = ('level',)


# EnergyLimit Modelini ro'yxatdan o'tkazish
@admin.register(EnergyLimit)
class EnergyLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'get_coin', 'energy_limit')
    list_filter = ('level',)


# RechargingSpeed Modelini ro'yxatdan o'tkazish
@admin.register(RechargingSpeed)
class RechargingSpeedAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'get_coin', 'recharging_speed')
    list_filter = ('level',)


# DailyBonus Modelini ro'yxatdan o'tkazish
@admin.register(DailyBonus)
class DailyBonusAdmin(admin.ModelAdmin):
    list_display = ('user', 'limit')


# BoostTap Modelini ro'yxatdan o'tkazish
@admin.register(BoostTap)
class BoostTapAdmin(admin.ModelAdmin):
    list_display = ('user', 'limit')


# UserTasks Modelini ro'yxatdan o'tkazish
@admin.register(UserTasks)
class UserTasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_complete', 'is_claimed')
    list_filter = ('is_complete', 'is_claimed')
    search_fields = ('user__user__full_name', 'task__name')

# Admins Modelini ro'yxatdan o'tkazish
@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ('user',)


# Voucher Modelini ro'yxatdan o'tkazish
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('name', 'coin', 'status')


# Voucher Modelini ro'yxatdan o'tkazish
@admin.register(VoucherUser)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher', 'user', 'is_claimed')
    list_filter = ('is_claimed',)

