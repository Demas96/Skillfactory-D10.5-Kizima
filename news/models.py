from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}'


    def update_rating(self):
        post_rating = Post.objects.filter(author_id=self).values('rating')
        post_rating = sum(rate['rating'] for rate in post_rating) * 3
        com_rating = Comment.objects.filter(user_id=self.pk).values('rating')
        com_rating = sum(rate['rating'] for rate in com_rating)
        compost_rating = Post.objects.filter(author_id=self.user_id).values('comment__rating')
        compost_rating = sum(rate['comment__rating'] for rate in compost_rating)
        self.rating = post_rating + com_rating + compost_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CategoryUser')

    def __str__(self):
        return f'{self.category}'

    def get_emails(self):
        result = set()
        for user in self.subscribers.all():
            result.add(user.email)
        return result


class Post(models.Model):
    article, new = 'AR', 'NE'
    TYPES = [(article, 'статья'), (new, 'новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    # def __str__(self):
    #     return f'{self}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        prv= self.text
        if len(prv) > 124:
            return prv[:124 - len(prv)] + '...'
        else:
            return prv


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.category}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
