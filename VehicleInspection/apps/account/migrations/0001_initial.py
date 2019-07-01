# Generated by Django 2.2.2 on 2019-06-25 07:48

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='验证码')),
                ('mobile', models.CharField(max_length=16, verbose_name='电话')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '短信验证码',
                'verbose_name_plural': '短信验证码',
                'db_table': 'VerifyCode',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(blank=True, help_text='手机号码', max_length=16, unique=True, verbose_name='移动电话')),
                ('name', models.CharField(blank=True, max_length=32, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, max_length=128, verbose_name='电子邮箱')),
                ('company', models.CharField(blank=True, max_length=128, verbose_name='所属公司')),
                ('usertype', models.CharField(choices=[('superadmin', '超级管理员'), ('stationadmin', '检查点管理员'), ('client', '普通用户')], default='client', max_length=16, verbose_name='用户类型')),
                ('avatar', models.URLField(blank=True, verbose_name='头像')),
                ('is_certificated', models.BooleanField(default=False, verbose_name='是否已完成实名认证')),
                ('credit', models.IntegerField(default=100, verbose_name='信用级别')),
                ('can_order', models.BooleanField(default=False, verbose_name='能否预约')),
                ('ban_start', models.DateTimeField(blank=True, null=True, verbose_name='开始封禁的时间')),
                ('ban_days', models.IntegerField(default=0, verbose_name='封禁天数')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'UserProfile',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
