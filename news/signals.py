import datetime
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post
from django.core.mail import EmailMultiAlternatives


@receiver(m2m_changed, sender=Post.category.through)
def send_mail(sender, instance, action, **kwargs):
    if action == 'post_add':
        html_content = render_to_string('msg_create.html', {'new_post': instance, })
        category = instance.category.all()
        emails = set()
        for cat in category:
            emails |= cat.get_emails()
        msg = EmailMultiAlternatives(
            subject=f'Здравствуй. Новая статья в твоём любимом разделе!',
            body=instance.text,
            from_email='dkizimasf@yandex.ru',
            to=emails,
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()


@receiver(pre_save, sender=Post)
def check_post_today(sender, instance, **kwargs):
    today_posts = Post.objects.filter(time_create__date=datetime.datetime.now().date())
    return len(today_posts)
