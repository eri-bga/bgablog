from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
import os
from django.utils import timezone

class CustomUser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None
    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=100, choices=STATUS, default='regular')
    profession = models.CharField(max_length=250)
    description = models.TextField(_('Description'), max_length=600, default='', blank=True)
    image = models.ImageField(_('Image'), default='default/user.png', upload_to=image_upload_to)
    
    def __str__(self) -> str:
        return self.username

class SubscribedUsers(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True, max_length=100)
    created_at = models.DateTimeField(_('Date created'), default=timezone.now)
    
    def __str__(self) -> str:
        return self.email