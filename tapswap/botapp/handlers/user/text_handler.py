from tapswap.utils import bot
from tapswap.botapp.keywords.inlines import start_inline_btn
from tapswap.models import *
from .utils import *


@bot.message_handler(commands=['start'], chat_types=['private'])
def echo_message(message):
    try:
        # Check if there's an invite code
        if len(message.text.split('f')) > 1:
            invite_code = message.text.split('f')[1].strip()
            user_exists = TelegramUser.objects.filter(tg_id=message.chat.id).exists()

            if not user_exists:
                create_user_data(message)

                try:
                    inviter = UserCoin.objects.get(user__tg_id=int(invite_code))
                    friend = Friend.objects.get(user=inviter)
                    friend.friends.add(InviteFriend.objects.create(user__tg_id=message.from_user.id))

                except TelegramUser.DoesNotExist:
                    print(f"Inviter with tg_id {invite_code} does not exist.")
                except Friend.DoesNotExist:
                    print(f"No Friends entry for user with tg_id {invite_code}.")

        else:
            user_exists = TelegramUser.objects.filter(tg_id=message.from_user.id).exists()
            if not user_exists:
                create_user_data(message)

        bot.send_message(message.chat.id, "Welcome to TabSwap {} !".format(message.from_user.full_name),
                         reply_markup=start_inline_btn())

    except Exception as e:
        import traceback
        print(f"An error occurred in message handler: {e}\n{traceback.format_exc()}")
