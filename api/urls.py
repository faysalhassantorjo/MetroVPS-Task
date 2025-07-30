from django.urls import path
from . import views


urlpatterns = [
    path('exchange-rate/', views.get_exchange_rate, name='get_exchange_rate'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('register/',views.RegisterUser.as_view())
]
