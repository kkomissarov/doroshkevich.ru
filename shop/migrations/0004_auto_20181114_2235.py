# Generated by Django 2.1.3 on 2018-11-14 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20181114_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='hidden_sort_order',
        ),
        migrations.RemoveField(
            model_name='category',
            name='sort_order',
        ),
    ]
