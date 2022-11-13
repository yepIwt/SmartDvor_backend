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