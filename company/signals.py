# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import UserInfo  
from .models import Post
from .tasks import send_matching_users_email

@receiver(post_save, sender=Post)
def notify_matching_users(sender, instance, **kwargs):
    post_skills = instance.skills.all()
    matching_users = UserInfo.objects.all()
    unique_emails = set()  

    for skill in post_skills:
        matching_users = matching_users.filter(skills=skill).distinct()

    subject = 'New Job Post Matching Your Skills'
    message = 'A new job post has been created that matches your skills and work time.'

    for user_info in matching_users:
        user = user_info.userId
        if user and user.email:
            unique_emails.add(user.email)  
    send_matching_users_email.delay(subject, message, list(unique_emails))