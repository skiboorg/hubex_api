from django.db import models
from equipment.services import create_random_string

class Status(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Статус '
        verbose_name_plural = 'Статус '

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Тип '
        verbose_name_plural = 'Тип '

    def __str__(self):
        return self.name


class InputField(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_boolean = models.BooleanField(default=False, null=True)
    is_input = models.BooleanField(default=False, null=True)
    is_date = models.BooleanField(default=False, null=True)

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

    class Meta:
        ordering = ('order_num',)
class Stage(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    role = models.ForeignKey('user.Role', on_delete=models.SET_NULL, blank=True, null=True)
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, blank=True, null=True)
    is_check_list_done = models.BooleanField(default=False, null=True)
    btn_1_goto_stage = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='goto_stage_1_btn')
    btn_1_label = models.CharField(max_length=255, blank=True, null=True)
    btn_2_goto_stage = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='goto_stage_2_btn')
    btn_2_label = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    number = models.CharField(max_length=255, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField('user.User',blank=True)
    is_critical = models.BooleanField(default=False, blank=True)
    object = models.ForeignKey('object.Object', on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.CASCADE, blank=True, null=True,related_name='orders')
    comment = models.TextField(blank=True, null=True)

    date_created_at = models.DateField(blank=True, null=True)
    date_assign_worker = models.DateField(blank=True, null=True)
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


class CheckListData(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)


class StageLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    new_stage = models.ForeignKey(Stage, on_delete=models.CASCADE, blank=True, null=True)





