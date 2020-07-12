# Generated by Django 3.0.7 on 2020-07-05 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_auto_20200705_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='ToBeSell',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='products',
            name='p_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
