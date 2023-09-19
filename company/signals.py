# # signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
# from api.models import UserInfo  # Import only UserInfo from the models
# from .models import Post  # Import the Post model

# @receiver(post_save, sender=Post)
# def notify_matching_users(sender, instance, **kwargs):
#     post_skills = instance.skills.all()

#     matching_users = UserInfo.objects.all()
#     unique_emails = set()  

#     for skill in post_skills:
#         matching_users = matching_users.filter(skills=skill).distinct()

#     subject = 'New Job Post Matching Your Skills'
#     message = 'A new job post has been created that matches your skills and work time.'

#     for user_info in matching_users:
#         user = user_info.userId
#         if user and user.email:
#             unique_emails.add(user.email)  
#     print(unique_emails)
#     for email in unique_emails:
#         print(email)
#         # send_mail(subject, message, 'your_email@example.com', [email], fail_silently=False)
