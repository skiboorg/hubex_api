from django.db.models.signals import post_save
import os
from django.conf import settings
from django.db import models

class OrderChat(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField('user.User',blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class OrderChatMessage(models.Model):
    chat = models.ForeignKey(OrderChat, blank=False, null=True, on_delete=models.CASCADE, verbose_name='В чате',
                             related_name='messages', db_index=True)
    user = models.ForeignKey('user.User', blank=False, null=True, on_delete=models.CASCADE,
                             verbose_name='Сообщение от', related_name='message_by_user')
    viewed_by = models.ManyToManyField('user.User', blank=True)
    message = models.TextField('Сообщение', blank=True,null=True)
    file = models.FileField('Файл к сообщению', upload_to='orderchat/', blank=True, null=True)
    file_name = models.CharField( max_length=255, blank=True, null=True)
    is_new = models.BooleanField('Не прочитанное сообщение', default=True)
    file_saved = models.BooleanField(default=False, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ('createdAt',)

    


def msg_post_save(sender, instance, created, **kwargs):
    if not instance.file_saved and instance.file:
        fullpath = os.path.join(settings.MEDIA_ROOT, instance.file.field.upload_to, instance.file.path)
        instance.size = os.path.getsize(fullpath)
        instance.file_saved = True
        instance.save()

post_save.connect(msg_post_save, sender=OrderChatMessage)