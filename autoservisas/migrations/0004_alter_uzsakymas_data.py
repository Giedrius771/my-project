# Generated by Django 4.2.2 on 2023-07-04 07:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0003_alter_automobiliomodelis_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uzsakymas',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
