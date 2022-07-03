import uuid
from django.db import models
from tutorials.models import Tutorial

class UserAvatar(models.Model):
    avatar = models.FileField(upload_to='media/uploads/avatar', blank=True)

    def __str__(self):
        return self.avatar.url

class CustomUser(models.Model):
    STATUS_CHOICES =(
    ('suscribed', 'Suscribed'),
    ('unsuscribed', 'Unsuscribed'),
    ('blocked', 'Blocked'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    suscribed =models.CharField(max_length=100, choices=STATUS_CHOICES, default='unsuscribed')
    token = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        success = False
        while not success:
            u_t = str(uuid.uuid4())
            if CustomUser.objects.filter(token = u_t):
                print(CustomUser.objects.filter(token = u_t))
                success = False
            else:
                super(CustomUser, self).save(*args, **kwargs)
                success = True
    def __str__(self):
        return self.name
    
class Message(models.Model):
    STATUS_CHOICES =(
    ('moderation', 'Moderation'),
    ('approved', 'Approved'),
    ('Decline', 'decline'),
    )
    room = models.ForeignKey(Tutorial, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    status =models.CharField(max_length=10, choices=STATUS_CHOICES, default='moderation')

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return f"{self.user.name} -> chats on -> {self.room.title}"