from django.db import models

class JobField(models.Model):
    field_name = models.CharField(max_length=255)

    def __str__(self):
        return self.field_name

class JobTitle(models.Model):
    title_name = models.CharField(max_length=255)
    field = models.ForeignKey(JobField, on_delete=models.CASCADE)

    def __str__(self):
        return self.title_name
    
# Languages

class Languages(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language
