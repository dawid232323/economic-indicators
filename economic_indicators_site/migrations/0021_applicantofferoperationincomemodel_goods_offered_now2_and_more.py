# Generated by Django 4.0.1 on 2022-02-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economic_indicators_site', '0020_rename_fullmarketanalisismodel_fullmarketanalysismodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantofferoperationincomemodel',
            name='goods_offered_now2',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='applicantofferoperationincomemodel',
            name='goods_offered_now3',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='applicantofferoperationincomemodel',
            name='goods_stopped1',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='applicantofferoperationincomemodel',
            name='goods_stopped2',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='applicantofferoperationincomemodel',
            name='goods_stopped3',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
