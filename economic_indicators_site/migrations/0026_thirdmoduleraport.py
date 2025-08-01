# Generated by Django 4.0.1 on 2022-02-28 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('economic_indicators_site', '0025_thirdmodulemaincomponentmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdModuleRaport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('identifier', models.CharField(max_length=10)),
                ('a1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a1', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a10', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a10', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a2', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a3', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a4', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a5', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a6', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a6', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a7', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a7', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a8', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a8', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('a9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a9', to='economic_indicators_site.thirdmodulemaincomponentmodel')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='economic_indicators_site.companysystemuser')),
            ],
        ),
    ]
