from django.contrib.sites.models import Site
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
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notification(instance.preview(), instance.pk, instance.title, subscribers)


# receiver(m2m_changed, sender=PostCategory)
#
#
# def notify_subscribers(sender, instance, action, **kwargs):
#     print(sender, instance, action, kwargs)
#     if action == 'post_add' and instance.__class__.__name__ == 'Post':
#         notify_subscribers_for_new_post(
#             instance.id, instance.title, instance.text
#         )
#
#
# def notify_subscribers_for_new_post(id, title, text):
#     site = Site.objects.get_current()
#     link = f'{settings.SITE_URL}news/{id}'
#
#     mailing_list = list(
#         PostCategory.objects.filter(
#             postThrough_id=id
#         ).values_list(
#             'categoryThrough__subscribers__username',
#             'categoryThrough__subscribers__first_name',
#             'categoryThrough__subscribers__email',
#             'categoryThrough__name',
#         )
#     )
#     print(mailing_list)
#
#
#     for user, first_name, email, category in mailing_list:
#         if not first_name:
#             first_name = user
#
#         html_content = render_to_string(
#             'post_created_email.html',
#             {
#                 'name': first_name,
#                 'category': category,
#                 'title': title,
#                 'text': text,
#                 'link': link,
#             }
#         )
#
#
#
#     message = EmailMultiAlternatives(
#         subject=f'{site.name}! '
#                 f'New post in category "{category}"',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[email]
#     )
#     message.attach_alternative(html_content, 'text.html')
#     message.send()
