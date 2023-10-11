from django.db import models
from api.models import *
from dashboard.models import *
# Create your models here.


class CompanyInfo(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100, null=True)
    company_size = models.CharField(max_length=100, null=True)
    company_type = models.CharField(max_length=100, null=True)
    gst = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    streetaddress = models.TextField(null=True)
    country = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    zipcode = models.BigIntegerField(null=True)
    is_verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    WORK_TIME_CHOICES = [
    ('short-term', 'short-term'),
    ('long-term', 'long-term'),
    ]
    EXPERIENCE_LEVEL_CHOICES = [
    ('fresher', 'fresher'),
    ('intermediate', 'intermediate'),
    ('export', 'export'),
    ]
    companyinfo = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,null=True)
    work_time = models.CharField(max_length=20,choices=WORK_TIME_CHOICES,default='long-term')
    job_category = models.ForeignKey(JobField,on_delete=models.CASCADE,null=True)
    Jobtitle = models.ForeignKey(JobTitle, on_delete=models.CASCADE,null=True)
    skills = models.ManyToManyField(Skills)
    level_of_experience = models.CharField(max_length=20,choices=EXPERIENCE_LEVEL_CHOICES,default='fresher')
    year_of_experience = models.BigIntegerField(blank=True,null=True)
    education = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

class ApplyJobs(models.Model):
    comanyInfo = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    userInfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    schedule = models.DateField(null=True, default=None) 
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class InviteUsers(models.Model):
    comanyInfo = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    userInfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)