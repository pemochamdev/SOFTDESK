from django.db import models

# Create your models here.

import os
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User Most Have An Email")
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super User Must Have is_taff = True")
        

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super User Must Have is_superuser = True")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    

    email = models.EmailField(_("email address"), unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email
    

def get_image_filename(instance, filename):

    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    avatar  = models.ImageField(upload_to=get_image_filename, blank=True)
    bio = models.CharField(max_length=400, blank=True)


    @property
    def filename(self):
        return os.path.basename(self.image.name)
    

    def __str__(self):
        return self.user.email