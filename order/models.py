import uuid
from django.db import models
from equipment.services import create_random_string
from colorfield.fields import ColorField
from django.db.models.signals import post_save
import os
from django.conf import settings

class Status(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    bg_color = ColorField(default='#FF0000')
    text_color = ColorField(default='#FFFFFF')
    is_default = models.BooleanField(default=False, null=True)
    is_done = models.BooleanField(default=False, blank=True)
    class Meta:
        verbose_name = 'Статус '
        verbose_name_plural = 'Статус '

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False, null=True)
    class Meta:
        verbose_name = 'Тип '
        verbose_name_plural = 'Тип '

    def __str__(self):
        return self.name


class InputField(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_boolean = models.BooleanField(default=False, null=True)
    is_boolean_with_input = models.BooleanField(default=False, null=True)
    is_multiple_boolean = models.BooleanField(default=False, null=True)
    is_multiple_boolean_with_input = models.BooleanField(default=False, null=True)
    is_input = models.BooleanField(default=False, null=True)
    is_separator = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name



class CheckList(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CheckListInput(models.Model):
    order_num = models.IntegerField(default=1, blank=True)
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, blank=True, null=True, related_name='inputs')
    input = models.ForeignKey(InputField, on_delete=models.CASCADE, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    labels = models.CharField(max_length=255, blank=True, null=True)
    input_data = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('order_num',)
class Stage(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    role = models.ForeignKey('user.Role', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, blank=True, null=True)
    is_default = models.BooleanField(default=False, null=True)

    need_add_user = models.BooleanField(default=False, null=True)
    is_add_user_required = models.BooleanField(default=False, null=True)
    add_user_role = models.ForeignKey('user.Role', on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='add_user_role')
    add_user_role_btn_label = models.CharField(max_length=255, blank=True, null=True)


    btn_1_goto_stage = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='goto_stage_1_btn')
    btn_1_label = models.CharField(max_length=255, blank=True, null=True)
    btn_2_goto_stage = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='goto_stage_2_btn')
    btn_2_label = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField('user.User',blank=True)
    is_critical = models.BooleanField(default=False, blank=True)
    object = models.ForeignKey('object.Object', on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.CASCADE, blank=True, null=True,related_name='orders')
    comment = models.TextField(blank=True, null=True)

    date_created_at = models.DateTimeField(auto_now_add=True, null=True)
    date_assign_worker = models.DateField(blank=True, null=True)
    date_done = models.DateField(blank=True, null=True)
    date_dead_line = models.DateField(blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True)
    is_time_left = models.BooleanField(default=False, blank=True)
    is_order_for_additional_equipment = models.BooleanField(default=False, blank=True)
    is_created_by_client = models.BooleanField(default=False, blank=True)
    class Meta:
        ordering = ('-is_critical','-date_created_at','is_done')
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка {self.number}'

    # def save(self, *args, **kwargs):
    #
    #     if not self.stage:
    #         self.stage = default_stage
    #     if not self.status:
    #         self.status = default_status
    #     self.type = default_type
    #     if not self.number:
    #
    #     super().save(*args, **kwargs)

def order_post_save(sender, instance, created, **kwargs):
    from user.models import Notification,User
    if created:
        default_stage = Stage.objects.get(is_default=True)
        default_type = Type.objects.get(is_default=True)
        default_status = Status.objects.get(is_default=True)

        number = 10000 + instance.id
        instance.number = number
        instance.stage = default_stage
        if not instance.type:
            instance.type = default_type
        instance.status = default_status
        instance.save()

        if instance.is_created_by_client:
            admin_users = User.objects.filter(is_staff=True)
            for user in admin_users:
                Notification.objects.create(
                    user=user,
                    link=f'/order/{instance.number}',
                    text=f'Создана заявка №{instance.number}',
                    order_number=instance.number
                )

post_save.connect(order_post_save, sender=Order)

class CheckListData(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='check_lists')
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class StageLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='stage_logs')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    new_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)


class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='files')
    file = models.FileField(upload_to='order/files', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f'{self.order.number}'


def obj_file_post_save(sender, instance, created, **kwargs):
    if created:
        fullpath = os.path.join(settings.MEDIA_ROOT, instance.file.field.upload_to, instance.file.path)
        instance.size = os.path.getsize(fullpath)
        instance.save()

post_save.connect(obj_file_post_save, sender=OrderFile)
