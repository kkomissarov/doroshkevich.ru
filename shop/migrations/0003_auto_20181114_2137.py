# Generated by Django 2.1.3 on 2018-11-14 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_category_sort_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='hidden_sort_order',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Порядок сортировки'),
        ),
        migrations.AlterField(
            model_name='category',
            name='sort_order',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Порядок сортировки'),
        ),
    ]
