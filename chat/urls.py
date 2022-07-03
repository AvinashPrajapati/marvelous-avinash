from django.urls import path
from .views import resend_or_recover, subscribe, verification

urlpatterns = [
    path('suscribe/', subscribe, name='subscribe'),
    path('resend-or-recover/', resend_or_recover, name='resend_or_recover'),
    path('verification/', verification, name='verification'),
]
