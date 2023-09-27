from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from dashboard.models import *

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'admin')

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

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
    role = models.CharField(max_length=30, default='user', choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_compleated = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


class Experience(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    Description = models.TextField()

class Education(models.Model):
    School = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    DatesAttended = models.DateField()
    Datesended = models.DateField()
    Description = models.TextField()

class UserInfo(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    experience = models.ManyToManyField(Experience)
    jobField = models.ForeignKey(JobField, on_delete=models.CASCADE,null=True)
    jobTitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE,null=True)
    skills = models.ManyToManyField(Skills)
    languages = models.ManyToManyField(Languages)
    education = models.ManyToManyField(Education)
    cv = models.FileField(upload_to='cv_uploads/',null=True, blank=True)
    streetaddress = models.TextField(null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    zipcode  = models.IntegerField(null=True)
    bio = models.TextField(null=True, default="Add bio")
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    path = models.CharField(max_length=100,default='/')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)