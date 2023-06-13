from django.db import models

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