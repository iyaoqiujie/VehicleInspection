# Generated by Django 2.2.2 on 2019-06-26 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0003_auto_20190626_1650'),
        ('appointment', '0002_auto_20190626_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppmntOrderAgg',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('scheduled_date', models.DateField(db_index=True, verbose_name='预约日期')),
                ('scheduled_time_period', models.CharField(max_length=32, verbose_name='预约时间区间')),
                ('order_count', models.SmallIntegerField(default=0, verbose_name='预约数')),
                ('station', models.ForeignKey(db_column='station_id', on_delete=django.db.models.deletion.CASCADE, related_name='appmntOrderAgg', to='station.InspStation', verbose_name='车辆检测站')),
            ],
            options={
                'verbose_name': '预约订单汇总',
                'verbose_name_plural': '预约订单汇总',
                'db_table': 'AppmntOrderAgg',
            },
        ),
    ]
