# Generated by Django 4.2.2 on 2023-07-12 20:40

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0013_automobilis_due_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='automobiliomodelis',
            name='description',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]
