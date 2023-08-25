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
    is_compleated = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Experience(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    description = models.TextField()


class UserInfo(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ManyToManyField(Experience)
