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
    is_new = models.BooleanField('Не прочитанное сообщение', default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('createdAt',)