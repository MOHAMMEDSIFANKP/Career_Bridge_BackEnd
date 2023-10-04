from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from api.models import *
@shared_task
def send_matching_users_email(subject, message, unique_emails):
    for email in unique_emails:
        to_email = email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.send()

@shared_task
def send_matching_users_notification(data):
    unique_id, message_for_notification = data
    path = '/user/'
    for id in unique_id:
        Notification.objects.create(user=id, message=message_for_notification, path=path)

@shared_task
def send_accepted_users_email( message, email):
    subject = 'Your are Selected'
    to_email = email
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()

@shared_task
def send_scheduled_users_email( message, email):
    subject = 'Your interview sheduled'
    to_email = email
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()