import os
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

class Object(models.Model):
    manager = models.ForeignKey('user.User',blank=True, null=True, on_delete=models.SET_NULL)
    number = models.CharField('Номер объекта\договора', max_length=255, blank=True, null=True, unique=True, db_index=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    longtitude = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    work_time = models.CharField('часы работы', max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, db_index=True)
    is_sign = models.BooleanField(default=False)
    is_have_other_additional_equipment = models.BooleanField(default=False, null=False)
    is_potencial = models.BooleanField(default=False)
    is_smart = models.BooleanField('стороннее управление (умный дом)', default=False)

    address_comment = models.TextField(blank=True, null=True)
    client = models.ForeignKey('client.Client',blank=True, null=True, on_delete=models.CASCADE,related_name='client_objects')
    image = models.FileField(upload_to='object/image', blank=True, null=True)
    # equipment = models.ManyToManyField('equipment.Equipment', blank=True)
    def __str__(self):
        return f'{self.number} - {self.address}'

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class ObjectFile(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='files')
    file = models.FileField(upload_to='object/images', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.object.name}'


def obj_file_post_save(sender, instance, created, **kwargs):
    if created:
        fullpath = os.path.join(settings.MEDIA_ROOT, instance.file.field.upload_to, instance.file.path)
        instance.size = os.path.getsize(fullpath)
        instance.save()

post_save.connect(obj_file_post_save, sender=ObjectFile)

class ObjectContact(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    name = models.CharField('ФИО', max_length=255, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=True, null=True)
    email = models.CharField('Email', max_length=255, blank=True, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    social = models.TextField('Соц сети',blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='contacts')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Контакт объекта'
        verbose_name_plural = 'Контакты объекта'


class AdditionalEquipmentCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        verbose_name = 'Категория Доп оборудование'
        verbose_name_plural = 'Категория Доп оборудование'

class AdditionalEquipmentModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(AdditionalEquipmentCategory, on_delete=models.CASCADE, blank=True, null=True, related_name='models')
    def __str__(self):
        return f'{self.name}'
    class Meta:
        verbose_name = 'Модель Доп оборудование'
        verbose_name_plural = 'Модель Доп оборудование'
class ObjectAdditionalEquipment(models.Model):
    amount = models.IntegerField(blank=True, null=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True, null=True, related_name='additional_equipments')
    model = models.ForeignKey(AdditionalEquipmentModel, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f'{self.model.category.name} {self.model.name} {self.amount}'

    class Meta:
        verbose_name = 'Доп оборудование'
        verbose_name_plural = 'Доп оборудование'