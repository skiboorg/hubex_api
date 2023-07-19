from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField('ИМЯ\НАЗВАНИЕ', max_length=255, blank=False, null=True)
    comment = models.TextField('КОММЕНТАРИЙ',blank=True, null=True)
    fiz = models.BooleanField('ФИЗ ЛИЦО?', default=False)
    dealer = models.BooleanField('Дилер?', default=False)
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


