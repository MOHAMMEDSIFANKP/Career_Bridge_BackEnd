from django.core.mail import EmailMessage
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

def send_verification_email(request, user):
    Users = User.objects.get(email=user.email)
    print(Users,'daxoooo')
    current_site = get_current_site(request)
    mail_subject = 'Please activate your account'
    message = render_to_string('user/activation_email.html', {
        'user': Users,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
