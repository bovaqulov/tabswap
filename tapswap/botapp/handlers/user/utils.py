from tapswap.models import TelegramUser


def create_user_data(message):
    user = TelegramUser.objects.get_or_create(
        tg_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )