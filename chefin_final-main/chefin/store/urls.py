from django.urls import path
from .views import *

urlpatterns = [
    path('rolu', rolu, name='rolu'),
    path('pizza', pizza, name='pizza'),
    path('salat', salat, name='salat'),
    path('osnovni', osnovni, name='osnovni'),
    path('soups', soups, name='soups'),
    path('zakyski', zakyski, name='zakyski'),
    path('garniry', garniry, name='garniry'),
    path('hot', hot, name='hot'),
    path('cold_drinks', cold_drinks, name='cold_drinks'),
    path('beer', beer, name='beer'),

    path('dostavka_ta_oplata', dostavka_ta_oplata, name='dostavka_ta_oplata'),
    path('zayvka', zayvka, name='zayvka'),
]
