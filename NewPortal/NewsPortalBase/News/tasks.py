from celery import shared_task
import time
import datetime
from django.core.mail import EmailMultiAlternatives
from NewsPortalBase import settings
from NewsPortalBase.settings import DEFAULT_FROM_EMAIL
from .models import Post, Category
from django.template.loader import render_to_string
from django.http import HttpResponse


@shared_task
def hello():
    time.sleep(10)
    print("Hello world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def mailing():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime__gte=last_week)
    categories = set(posts.values_list('dopCategory__categories', flat=True))
    subscribers = set(Category.objects.filter(categories__in=categories).values_list('subscribers__email', flat=True))
    html_contex = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Интересное за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_contex, 'text/html')
    msg.send()
    return HttpResponse("Еженедельные новости отправлены успешно!")


@shared_task
def notifications(pk):
    post = Post.objects.get(pk=pk)
    categories = post.dopCategory.all()
    title = post.heading
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("Новая новость отправлена успешно!")
