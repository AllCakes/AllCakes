
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeManage', '0015_auto_20211119_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='locationGu',
            field=models.CharField(default='노원구', max_length=10, verbose_name='구'),
        ),
    ]
