import segno
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import uuid
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from django.db.models.signals import post_save
from .services import create_random_string

class Client(models.Model):
    name = models.CharField('ИМЯ\НАЗВАНИЕ', max_length=255, blank=False, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    fiz = models.BooleanField('ФИЗ ЛИЦО?', default=False)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ClientContact(models.Model):
    name = models.CharField('ИМЯ', max_length=255, blank=False, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=False, null=True)
    email = models.CharField('Email', max_length=255, blank=False, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    social = models.TextField('Соц сети',blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='contacts')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Контакт клиента'
        verbose_name_plural = 'Контакты клиента'


class Object(models.Model):
    number = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    address_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class ObjectImage(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='images')
    image = models.FileField(upload_to='object/images', blank=True, null=True)
    def __str__(self):
        return f'{self.object.name}'



class ObjectContact(models.Model):
    name = models.CharField('ИМЯ', max_length=255, blank=False, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=False, null=True)
    email = models.CharField('Email', max_length=255, blank=False, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    social = models.TextField('Соц сети',blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='contacts')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Контакт объекта'
        verbose_name_plural = 'Контакты объекта'


class EquipmentModel(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    image = models.FileField(upload_to='equipment/', blank=True, null=True)

    class Meta:
        verbose_name = 'Модель оборудования'
        verbose_name_plural = 'Модель оборудования'

class EquipmentFirm(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        verbose_name = 'Фирма оборудования'
        verbose_name_plural = 'Фирма оборудования'


class Equipment(models.Model):
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE, blank=True, null=True)
    firm = models.ForeignKey(EquipmentFirm, on_delete=models.CASCADE, blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='equipments')
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    qr = models.FileField(upload_to='equipment/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    date_in_work = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        serial_number = f'{create_random_string(3)}-{create_random_string(5)}-{create_random_string(True,2)}'
        if not self.serial_number:
            self.serial_number = serial_number
        if not self.qr:
            qr = segno.make_qr(f'http://79.132.139.252:9090/equipment/qr/{serial_number}', version=23, error='L', mask=3)
            path = f'{settings.MEDIA_ROOT}/equipment/{serial_number}.png'
            qr.save(path, scale=10, dark=(0, 0, 0,), light=(240, 240, 240), border=0)
            self.qr = f'equipment/{serial_number}.png'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

class OrderType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Тип заявки'


class OrderStatus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статус заявки'

class OrderWorkType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Вид работ'
        verbose_name_plural = 'Вид работ'



class Order(models.Model):
    number = models.CharField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(OrderType, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, blank=True, null=True)
    is_critical = models.BooleanField(default=False, blank=True)
    work_type = models.ForeignKey(OrderWorkType, on_delete=models.CASCADE, blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True,related_name='orders')
    comment = models.TextField(blank=True, null=True)
    worker = models.ForeignKey('user.User', on_delete=models.SET_NULL, blank=True, null=True)

    date_created_at = models.DateField(blank=True, null=True)
    date_assing_worker = models.DateField(blank=True, null=True)
    date_done = models.DateField(blank=True, null=True)
    date_dead_line = models.DateField(blank=True, null=True)
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def save(self, *args, **kwargs):
        number = f'{create_random_string(3)}-{create_random_string(5)}-{create_random_string(digits=False,num=2)}'
        if not self.number:
            self.number = number
        super().save(*args, **kwargs)



