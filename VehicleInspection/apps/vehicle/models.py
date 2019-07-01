from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vehicle(models.Model):
    CHARACTER_CHOICES = (
        (1, '非营运'),
        (2, '营运')
    )
    id = models.BigAutoField(primary_key=True)
    bound_user = models.ForeignKey(User, related_name='boundVehicles', on_delete=models.CASCADE,
                                   db_column='user_id', null=True, blank=True, verbose_name='绑定车主')
    vin = models.CharField(verbose_name='车辆识别代码', max_length=32, unique=True)
    plate = models.CharField(verbose_name='车牌号', max_length=16, unique=True)
    vtype = models.CharField(verbose_name='车辆类型', max_length=16, blank=True)
    owner = models.CharField(verbose_name='所有人', max_length=16, blank=True)
    character = models.IntegerField(verbose_name='使用性质', choices=CHARACTER_CHOICES, default=1)
    created = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'vehicle'
        verbose_name = '机动车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '车牌号:[{}], 车辆识别代码: [{}]'.format(self.plate, self.vin)
