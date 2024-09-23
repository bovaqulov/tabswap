
from django.contrib import admin
from django.urls import path
from tapswap.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', telegram_webhook, name='telegram_webhook'),

    path('api/v1/main-page/<int:user_id>/', EarnPageView.as_view()),
    path('api/v1/tasks/<int:user_id>/', TaskPageView.as_view()),
    path('api/v1/tasks-complete/<int:user_id>/', TaskCompleteView.as_view()),
    path('api/v1/tasks-claimed/<int:user_id>/', TaskClaimView.as_view()),
    path('api/v1/friends/<int:user_id>/', FriendsPageView.as_view()),
    path('api/v1/boosts/<int:user_id>/', BoostsPageView.as_view()),
    path('api/v1/boosters/<int:user_id>/', BoostersPageView.as_view()),
    path('api/v1/vouchers/<int:user_id>/', VoucherPageView.as_view()),
]

