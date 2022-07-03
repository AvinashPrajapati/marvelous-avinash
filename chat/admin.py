from django.contrib import admin

# Register your models here.
from .models import CustomUser, Message, UserAvatar

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'suscribed')
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','room', 'user', 'date_added')




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserAvatar)
