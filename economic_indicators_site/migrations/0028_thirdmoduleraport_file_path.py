# Generated by Django 4.0.1 on 2022-02-28 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('economic_indicators_site', '0027_alter_thirdmodulemaincomponentmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='thirdmoduleraport',
            name='file_path',
            field=models.FilePathField(db_index=True, null=True),
        ),
    ]
