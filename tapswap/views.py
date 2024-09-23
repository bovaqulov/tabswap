import os
import json
import django
import telebot

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import tapswap.botapp.handlers
from .models import *
from .utils import check_member, bot


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabswap.settings')

django.setup()



@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            update_data = json.loads(request.body.decode('UTF-8'))

            update = telebot.types.Update.de_json(update_data)

            bot.process_new_updates([update])

            return JsonResponse({"status": "ok"})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return HttpResponse("<h1>Admin</h1>", content_type='text/html')
    # Call any middleware or setup functions






# EARN PAGE
class EarnPageView(APIView):


    def get(self, request, user_id):
        # `UserCoin` modelidagi `user__tg_id` maydoniga mos ravishda foydalanuvchini olish
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        # API orqali javob ma'lumotlarini tayyorlash
        data = {
            "user_coin": user_coin.coin,
            "add_coin": user_coin.add,
            "max_coin": user_coin.max_coin,
        }
        return Response(data, status=status.HTTP_200_OK)


    def put(self, request, user_id, *args, **kwargs):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        add_coin = int(request.query_params.get("add_coin", user_coin.add))

        if user_coin.max_coin <= 0:
            return Response({
                "user_coin": user_coin.coin,
                "add_coin": add_coin,
                "max_coin": user_coin.max_coin,
            }, status=status.HTTP_400_BAD_REQUEST)

        if user_coin.max_coin > add_coin:
            user_coin.max_coin -= add_coin
            user_coin.coin += add_coin
        else:
            user_coin.coin += user_coin.max_coin
            user_coin.max_coin = 0


        user_coin.save()

        data = {
            "user_coin": user_coin.coin,
            "add_coin": add_coin,
            "max_coin": user_coin.max_coin,
        }
        return Response(data, status=status.HTTP_200_OK)


# TASK PAGE
class TaskPageView(APIView):
    def get(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        # UserTasks modelidan foydalangan holda foydalanuvchiga bog'langan vazifalarni olish
        user_tasks = UserTasks.objects.filter(user=user_coin, task__outtime__gt=timezone.now())

        task_list = [
            {
                "task_pk": user_task.task.pk,
                "task_name": user_task.task.name,
                "task_coin": user_task.task.coin,
                "task_link": user_task.task.link,
                "task_type": user_task.task.type,
                "is_complete": user_task.is_complete,
                "is_claimed": user_task.is_claimed,
            } for user_task in user_tasks
        ]

        data = {
            "user_coin": user_coin.coin,
            "tasks": task_list,
        }
        return Response(data, status=status.HTTP_200_OK)


class TaskCompleteView(APIView):

    def put(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        task_id = request.query_params.get("task_pk")

        user_task = get_object_or_404(UserTasks, task__pk=task_id, user=user_coin)

        if user_task.task.type == "telegram":
            user_task.is_complete = check_member(user_task.task.link, user_id)
        else:
            user_task.is_complete = True

        user_task.save()

        return Response({"is_complete": user_task.is_complete}, status=status.HTTP_200_OK)


class TaskClaimView(APIView):
    def put(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)
        task_id = request.query_params.get("task_pk")

        user_task = get_object_or_404(UserTasks, task__pk=int(task_id), user=user_coin)

        if user_task.is_complete and user_task.is_claimed == False:

            user_coin.coin += user_task.task.coin
            user_coin.save()

            user_task.is_claimed = True
            user_task.save()
            return Response({"is_claimed": True, "message": "claimed"}, status=status.HTTP_200_OK)

        elif user_task.is_claimed:
            return Response({"is_claimed": True, "message": "no claimed"}, status=status.HTTP_200_OK)

        else:
            return Response({"is_claimed": False}, status=status.HTTP_400_BAD_REQUEST)


# FRIENDS PAGE
class FriendsPageView(APIView):
    def get(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)
        friends = get_object_or_404(Friend, user=user_coin)

        friends_data = []
        if friends.invited_friends.exists():
            for invited_friend in friends.invited_friends.all():
                friends_data.append({
                    "name": invited_friend.user.user.full_name,
                    "is_done": invited_friend.is_done,
                    "get_coin": invited_friend.coin,
                    "friend_pk": invited_friend.pk,
                })

        data = {
            "link": friends.link,
            "user_coin": user_coin.coin,
            "user_count": friends.invited_friends.count(),
            "friends": friends_data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)
        friend_pk = request.query_params.get("friend_pk")
        is_done = request.query_params.get("is_done")

        invite_friend = InviteFriend.objects.filter(pk=int(friend_pk)).first()

        if invite_friend is None:
            return Response({"message": "InviteFriend does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if is_done == "true" and not invite_friend.is_done == True:
            user_coin.coin += invite_friend.coin
            invite_friend.is_done = True
            invite_friend.save()
            user_coin.save()

            return Response({"message": "added"}, status=status.HTTP_200_OK)

        elif invite_friend.is_done == True:
            return Response({"message": "no added"}, status=status.HTTP_200_OK)


        return Response({"message": "not updated"}, status=status.HTTP_400_BAD_REQUEST)


# BOOST PAGE
class BoostsPageView(APIView):
    def get(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)
        multitap = Multitap.objects.get(user=user_coin)
        energy_limit = EnergyLimit.objects.get(user=user_coin)
        daily_bonus = DailyBonus.objects.get(user=user_coin)
        boost_tap = BoostTap.objects.get(user=user_coin)
        recharging_speed = RechargingSpeed.objects.get(user=user_coin)

        data = {
            "user_coin": user_coin.coin,
            "energy_full": daily_bonus.limit,
            "boost_tap": boost_tap.limit,
            "multitap": {
                "level": multitap.level,
                "coin": multitap.get_coin
            },
            "energy_limit": {
                "level": energy_limit.level,
                "coin": energy_limit.get_coin
            },
            "recharging_speed": {
                "level": recharging_speed.level,
                "coin": recharging_speed.get_coin
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class BoostersPageView(APIView):
    def put(self, request, user_id):
        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)

        boost_type = request.query_params.get("type")

        if boost_type == "multitap":
            user_coin.add += 1
            boost_type_name = Multitap.objects.get(user=user_coin)

        elif boost_type == "energy_limit":
            boost_type_name = EnergyLimit.objects.get(user=user_coin)
            user_coin.limit *= user_coin.limit
        else:
            boost_type_name = RechargingSpeed.objects.get(user=user_coin)
            boost_type_name.recharging_speed *= 1.5

        if boost_type_name.get_coin <= user_coin.coin:
            boost_type_name.level += 1

            boost_type_name.get_coin *= 2
            boost_type_name.save()

            user_coin.coin -= boost_type_name.get_coin
            user_coin.save()

            return Response({
                "user_coin": user_coin.coin,
                f"{boost_type}": {
                    "level": boost_type_name.level,
                    "coin": boost_type_name.get_coin,
                }
            }, status=status.HTTP_200_OK)

        return Response({"message": "not enough coin", "user_coin": user_coin.coin}, status=status.HTTP_400_BAD_REQUEST)


#BANK PAGE
class VoucherPageView(APIView):

    def get(self, request, user_id):
        vouchers = Voucher.objects.filter(status=True)
        voucher_list = []
        for voucher in vouchers:
            voucher_list.append({
                "id": voucher.id,
                "name": voucher.name,
                "coin": voucher.coin,
                'som': voucher.som,

            })
        data = {
            "voucher_count": vouchers.count(),
            "vouchers": voucher_list,
        }
        return Response(data, status=status.HTTP_200_OK)


    def put(self, request, user_id):

        user_coin = get_object_or_404(UserCoin, user__tg_id=user_id)
        voucher_pk = request.query_params.get("voucher_id")
        voucher = Voucher.objects.get(pk=voucher_pk)
        try:
            if voucher.coin < user_coin.coin:
                user_coin.coin -= voucher.coin
                user_coin.save()

                VoucherUser.objects.create(
                    user=user_coin,
                    voucher=voucher
                )

                admins = '\nadmin: @'.join([str(a.user.user.username) for a in Admins.objects.all()])

                try:
                    bot.send_message(user_id, text=f"""
    Assalomu alaykum sizning so'rovingiz qabul qilindi !
    
    Agar savollar bo'lsa adminlarimizga murojat qiling
    
    {admins}
    """)

                except Exception as e:
                    return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                for user in Admins.objects.all():

                    bot.send_message(user.user.user.tg_id, text=f"""
    Name: {user_coin.user.full_name}
    Username: @{user_coin.user.username}
    Coin: {user_coin.coin}
    Vouchers: {voucher.coin}
    """)
                return Response({"message": "ok"}, status=status.HTTP_200_OK)

            return Response({"message": "No coin"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
