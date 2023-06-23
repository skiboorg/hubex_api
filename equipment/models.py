from django.db import models
from .services import create_random_string
import segno
from django.conf import settings

# Create your models here.
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
    object = models.ForeignKey('object.Object', on_delete=models.CASCADE, blank=True, null=True, related_name='equipments')
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    qr = models.FileField(upload_to='equipment/', blank=True, null=True, editable=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    date_in_work = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.serial_number} - {self.name}'

    def save(self, *args, **kwargs):
        # serial_number = f'{create_random_string(3)}-{create_random_string(5)}-{create_random_string(True,2)}'
        if not self.qr:
            # self.serial_number = serial_number
            qr = segno.make_qr(f'http://91.228.155.186:9000/equipment/qr/{self.serial_number}', version=23, error='L', mask=3)
            path = f'{settings.MEDIA_ROOT}/equipment/{self.serial_number}.png'
            qr.save(path, scale=10, dark=(0, 0, 0,), light=(240, 240, 240), border=0)
            self.qr = f'equipment/{self.serial_number}.png'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
