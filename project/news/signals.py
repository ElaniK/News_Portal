from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Post
from project import settings


def send_notification(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text.html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['actions'] == 'post_add':
        categories = instance.categoryThrough.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers)
