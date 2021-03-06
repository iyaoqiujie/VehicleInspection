# Generated by Django 2.2.2 on 2019-06-26 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentOrder',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('scheduled_date', models.DateField(verbose_name='预约日期')),
                ('scheduled_time_period', models.CharField(max_length=32, verbose_name='预约时间区间')),
                ('service', models.CharField(choices=[('INSPECTION', '检测'), ('REPAIR', '维修')], default='INSPECTION', max_length=16, verbose_name='预约服务')),
                ('status', models.CharField(choices=[('PENDING', '待审核'), ('REJECTED', '已拒绝'), ('ACTIVE', '进行中'), ('CANCELED', '已取消'), ('COMPLETED', '已完成')], default='PENDING', max_length=16, verbose_name='预约订单状态')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='预约订单创建时间')),
                ('order_user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='appointmentOrders', to=settings.AUTH_USER_MODEL, verbose_name='预约客户')),
                ('station', models.ForeignKey(db_column='station_id', on_delete=django.db.models.deletion.CASCADE, related_name='appointmentOrders', to='station.InspStation', verbose_name='车辆检测站')),
            ],
            options={
                'verbose_name': '预约订单',
                'verbose_name_plural': '预约订单',
                'db_table': 'AppointmentOrder',
            },
        ),
    ]
