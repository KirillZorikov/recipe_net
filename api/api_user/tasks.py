from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


@shared_task
def send_instructions(email_to, url):
    subject = 'Your password has been reset'
    message = f'To change your password, follow the link: {url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_to]
    send_mail(subject, message, email_from, recipient_list)

@shared_task
def inform_admins():
    User = get_user_model()
    admins = User.objects.filter(is_staff=True).values('email')
    date = datetime.now() - timedelta(days=1)
    users = User.objects.filter(date_joined__gte=date)
    subject = 'New users today'
    if users:
        message = 'Registered today:\n'
    else:
        message = f'No one has registered today :('
    for user in users:
        message += user.username + '\n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [admin['email'] for admin in admins]
    send_mail(subject, message, email_from, recipient_list)
