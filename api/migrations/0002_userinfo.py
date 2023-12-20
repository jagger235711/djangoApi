# Generated by Django 4.2.6 on 2023-12-19 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('gender', models.CharField(choices=[('1', '男'), ('2', '女')], max_length=8, verbose_name='性别')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.depart', verbose_name='部门')),
            ],
        ),
    ]
