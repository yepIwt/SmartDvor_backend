from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here. Okay.


class User(AbstractUser):
    username = models.CharField("Короткая ссылка", max_length = 255, unique = True)
    email = models.CharField("Email", max_length = 255, unique = True)
    password = models.CharField("Пароль", max_length = 255)
    address = models.CharField("Адрес", max_length = 255)
    sex = models.CharField("Пол человека", max_length = 8)
    birthday = models.DateField("Дата рождения", default = datetime.date.today())

    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)

    def age(self):
        date = self.birthday
        return datetime.date.today().year - date.year - ((datetime.date.today().month, datetime.date.today().day) < (date.month, date.day))

class Post(models.Model):
    post_title = models.CharField("Название поста", max_length = 200)
    post_text = models.TextField("Текст поста")
    pub_date = models.DateTimeField("Дата создания поста", default = datetime.datetime.today)
    post_author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.post_author.username}: '{self.post_title}'"

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_text = models.CharField("Текст комментария", max_length = 200)
    comment_author = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField("Дата создания комментария", default = datetime.datetime.today)

    def __str__(self):
        return f"{self.comment_author.username}: {self.post.post_title} - {self.comment_text}"