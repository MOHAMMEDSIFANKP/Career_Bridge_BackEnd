from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from .models import User
from django.contrib.sites.models import Site

@shared_task
def send_activation_email(user_email, user_pk):
    # Construct and send the activation email
    user = User.objects.get(pk=user_pk)
    current_site = Site.objects.get_current()
    mail_subject = 'Please activate your account'
    message = render_to_string('user/activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'cite': current_site
    })
    to_email = user_email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

@shared_task
def send_forgotpassword_email(email):
    user = User.objects.get(email=email)
    current_site = Site.objects.get_current()
    mail_subject = 'Reset your password'
    message = render_to_string('user/forgot_password.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'cite': current_site
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
