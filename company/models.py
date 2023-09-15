from django.db import models
from api.models import User
# Create your models here.

class CompanyInfo(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100,null=True)
    company_size = models.CharField(max_length=100,null=True)
    company_type = models.CharField(max_length=100,null=True)
    gst = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    is_verify = models.BooleanField(default=False)

