# Generated by Django 2.2.2 on 2019-06-26 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspstation',
            name='admin',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='stationAdmin', to=settings.AUTH_USER_MODEL, verbose_name='管理员'),
            preserve_default=False,
        ),
    ]
