from django.db import models
from django.contrib.auth.models import User
from config import *
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postR = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating')

        commentR = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_R = 0
        c_R += commentR.get('commentRating')

        self.rating = p_R * 3 + c_R
        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    categories = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.categories}"


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_NEWS, default=ARTICLE)
    datetime = models.DateTimeField(auto_now_add=True)
    dopCategory = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        dataf = 'Post from {}'.format(self.datetime.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.heading}"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post},from the category:  {self.category}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creatureComment = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.creatureComment}, {self.user}"

