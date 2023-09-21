from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage

@shared_task
def send_matching_users_email(subject, message, unique_emails):
    for email in unique_emails:
        to_email = email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.send()




 