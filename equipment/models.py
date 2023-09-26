from django.db import models
from .services import *
import segno
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
# Create your models here.


class EquipmentFirm(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Фирма оборудования'
        verbose_name_plural = 'Фирма оборудования'

class EquipmentModel(models.Model):
    firm = models.ForeignKey(EquipmentFirm, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    image = models.FileField(upload_to='equipment/', blank=True, null=True)
    file = models.FileField(upload_to='equipment/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    show_to_client = models.BooleanField(default=False, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} | Фирма: {self.firm}'

    class Meta:
        verbose_name = 'Модель оборудования'
        verbose_name_plural = 'Модель оборудования'


class Equipment(models.Model):
    model = models.ForeignKey(EquipmentModel, on_delete=models.CASCADE, blank=True, null=True)
    object = models.ForeignKey('object.Object', on_delete=models.CASCADE, blank=True, null=True, related_name='equipments')
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    qr = models.FileField(upload_to='equipment/', blank=True, null=True, editable=True)
    qr_with_info = models.FileField(upload_to='equipment/', blank=True, null=True, editable=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    date_in_work = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    is_warranty = models.BooleanField(default=False, blank=True)
    is_service_book_sign = models.BooleanField(default=False, blank=True)
    is_at_exchange = models.BooleanField(default=False, blank=True)
    warranty_ends = models.DateField(blank=True, null=True)
    service_book_sign_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return f'S/N :{self.serial_number} | Название :{self.name}'

    def save(self, *args, **kwargs):
        # serial_number = f'{create_random_string(3)}-{create_random_string(5)}-{create_random_string(True,2)}'
        if not self.qr:
            data = f"http://buhler.onside.software/equipment/qr/{self.serial_number}"
            qr_content = generate_styled_qrcode(data)
            path = f'{settings.MEDIA_ROOT}/equipment/{self.serial_number}.png'
            with open(path, 'wb') as f:
                f.write(qr_content)
            self.qr = f'equipment/{self.serial_number}.png'

        # if not self.qr_with_info:
        #     qr_with_info = make_info_qr(qr_content,'МОДЕЛЬ',self.model.name,'СЕРИЙНЫЙ НОМЕР',self.serial_number)
        #     qr_with_info.save(f'{settings.MEDIA_ROOT}/equipment/{self.id}.jpg')
        #     self.qr_with_info=f'/equipment/{self.id}.jpg'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
