# Generated by Django 4.0.1 on 2022-02-04 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('economic_indicators_site', '0003_fullraport_companysystemuser_num_of_reports_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedassets',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
