# Generated by Django 4.2.2 on 2023-07-12 20:56

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0014_automobiliomodelis_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automobiliomodelis',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
