# Generated by Django 3.0.5 on 2020-04-19 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Url', '0004_auto_20200418_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hit',
            options={'ordering': ['click_date'], 'verbose_name': 'Доп информация', 'verbose_name_plural': 'Доп информации'},
        ),
    ]
