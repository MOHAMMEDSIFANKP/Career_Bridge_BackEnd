from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('company', 'company'),
        ('admin', 'admin')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    role = models.CharField( max_length=30, default='user', choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
