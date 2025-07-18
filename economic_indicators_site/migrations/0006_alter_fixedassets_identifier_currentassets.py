# Generated by Django 4.0.1 on 2022-02-04 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economic_indicators_site', '0005_fixedassets_identifier_alter_fixedassets_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedassets',
            name='identifier',
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.CreateModel(
            name='CurrentAssets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_period', models.IntegerField()),
                ('identifier', models.CharField(db_index=True, max_length=10)),
                ('materials_resources', models.FloatField(default=0)),
                ('products_halfproducts_in_progress', models.FloatField(default=0)),
                ('ready_products', models.FloatField(default=0)),
                ('goods', models.FloatField(default=0)),
                ('other_supplies', models.IntegerField(default=0)),
                ('delivery_debts', models.FloatField(default=0)),
                ('owner_debts', models.FloatField(default=0)),
                ('money', models.FloatField(default=0)),
                ('other_assets', models.FloatField(default=0)),
                ('sum_of_supplies', models.FloatField()),
                ('sum_of_debts', models.FloatField()),
                ('sum_of_current_assets', models.FloatField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='economic_indicators_site.companysystemuser')),
            ],
        ),
    ]
