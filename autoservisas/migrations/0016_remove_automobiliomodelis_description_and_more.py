# Generated by Django 4.2.2 on 2023-07-13 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0015_alter_automobiliomodelis_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='automobiliomodelis',
            name='description',
        ),
        migrations.AddField(
            model_name='automobilis',
            name='description',
            field=models.CharField(default='Some default value', max_length=255),
        ),
    ]