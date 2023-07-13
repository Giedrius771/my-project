# Generated by Django 4.2.2 on 2023-07-04 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0002_delete_genre_paslauga_datetime_now'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='automobiliomodelis',
            options={'verbose_name': 'Automobilio modelis', 'verbose_name_plural': 'Automobilio modeliai'},
        ),
        migrations.AlterModelOptions(
            name='automobilis',
            options={'verbose_name': 'Automobilis', 'verbose_name_plural': 'Automobiliai'},
        ),
        migrations.AlterModelOptions(
            name='paslauga',
            options={'verbose_name': 'Paslauga', 'verbose_name_plural': 'Paslaugos'},
        ),
        migrations.AlterModelOptions(
            name='uzsakymas',
            options={'verbose_name': 'Užsakymas', 'verbose_name_plural': 'Užsakymai'},
        ),
        migrations.AlterModelOptions(
            name='uzsakymoeilute',
            options={'verbose_name': 'Užsakymo eilutė', 'verbose_name_plural': 'Užsakymo eilutės'},
        ),
        migrations.RemoveField(
            model_name='paslauga',
            name='datetime_now',
        ),
        migrations.AlterField(
            model_name='automobiliomodelis',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='automobilis',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='paslauga',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='uzsakymas',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='uzsakymoeilute',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
