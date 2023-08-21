import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from datetime import timedelta
# from .tasks import send_email

import logging
logger = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, password, **extra_fields):
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login, password, **extra_fields)

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(login, password, **extra_fields)


class PagePermission(models.Model):
    name = models.CharField('Название доступа', max_length=20, blank=True, null=True)
    can_open = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class Page(models.Model):
    name = models.CharField('Название', max_length=20, blank=True, null=True)
    url = models.CharField('Ссылка на страницу', max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)

class Role(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class RolePage(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, related_name='pages')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, null=True)
    permission = models.ForeignKey(PagePermission, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.role.name} - {self.page.name} - {self.permission.name}'
class User(AbstractUser):
    username = None
    firstname = None
    lastname = None
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    login = models.CharField('Логин', max_length=255, blank=True, null=True, unique=True)
    email = models.CharField('Почта', max_length=255, blank=True, null=True)
    fio = models.CharField('ФИО', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=True, null=True)
    plain_password = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.FileField(upload_to='usr/ava',blank=True, null=True)
    is_driving = models.BooleanField(default=False, blank=True)
    is_online = models.BooleanField('Онлайн', default=False)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    subscription_info = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f'{self.fio} - {self.role.name if self.role else "нет роли"}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '1. Пользователи'


def user_post_save(sender, instance, created, **kwargs):
    #import monthdelta
    #datetime.date.today() + monthdelta.monthdelta(months=1)

    if created:
        print('created')


post_save.connect(user_post_save, sender=User)


class UserWorkTimeType(models.Model):
    name = models.CharField('Название', max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name

class UserWorkTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='work_time')
    type = models.ForeignKey(UserWorkTimeType, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_hidden = models.BooleanField(default=False, null=False)
    class Meta:
        ordering = ('date','start_time')


class Notification(models.Model):
    order_number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    text = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


