# Generated by Django 3.2.5 on 2022-02-04 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeManage', '0006_auto_20220203_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='color',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='cake',
            name='cream',
            field=models.JSONField(default=dict),
        ),
    ]