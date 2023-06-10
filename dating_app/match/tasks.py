from celery import shared_task
from django.core.mail import send_mail


@shared_task
def match_notification(sender_name, sender_email,
                       liked_user_name, liked_user_email):
    """Задача на отправку e-mail при взаимной симпатии участников."""
    subject = 'Dating App: вы понравились!'
    message = (f'{liked_user_name}, добрый день!,\n\n'
               f'Вы понравились участнику по имени {sender_name}! '
               f'Почта участника: {sender_email}.\n\n'
               'С любовью,\n'
               'Ваш Dating App!')
    return send_mail(subject,
                     message,
                     'client_service@dating_app.com',
                     [liked_user_email])
