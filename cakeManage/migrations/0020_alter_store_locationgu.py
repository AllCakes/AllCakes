# Generated by Django 3.2.5 on 2021-11-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeManage', '0019_merge_20211121_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='locationGu',
            field=models.CharField(default='00구/00시', max_length=10, verbose_name='지역(구/시)'),
        ),
    ]
