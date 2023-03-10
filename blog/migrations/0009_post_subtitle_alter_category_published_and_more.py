# Generated by Django 4.1.5 on 2023-01-20 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_category_image_alter_category_published_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default='', max_length=250, verbose_name='Subtitle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 20, 18, 11, 57, 181003, tzinfo=datetime.timezone.utc), verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 20, 18, 11, 57, 181656, tzinfo=datetime.timezone.utc)),
        ),
    ]
