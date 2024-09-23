from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils import timezone
from .models import Task, UserCoin


# Create your tests here.
class SwapTestCase(TestCase):
    def setUp(self):

        # Foydalanuvchi ID sini belgilash
        user_id = "user_id_ni_bu_yerda_qo'ying"
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        # Olish
        tasks = Task.objects.filter(assigned_users=user_coin)
        print(f"Assigned tasks: {tasks}")

        # Olish va vaqtni tekshirish
        tasks_valid_time = tasks.filter(outtime__gt=timezone.now())
        print(f"Tasks with valid outtime: {tasks_valid_time}")