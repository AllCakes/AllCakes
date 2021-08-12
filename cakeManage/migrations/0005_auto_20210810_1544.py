# Generated by Django 3.2.5 on 2021-08-10 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cakeManage', '0004_auto_20210810_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_accepted',
            field=models.BooleanField(default=False, verbose_name='가게 승인'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='진행중'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='결제완료'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='주문 날짜'),
        ),
        migrations.AlterField(
            model_name='order',
            name='referred_cake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.cake', verbose_name='선택 케이크'),
        ),
        migrations.AlterField(
            model_name='order',
            name='referred_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cakeManage.store', verbose_name='가게'),
        ),
        migrations.AlterField(
            model_name='order',
            name='reviewing',
            field=models.IntegerField(default=1, verbose_name='(평점)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='주문자'),
        ),
    ]