# Generated by Django 4.1.5 on 2023-01-21 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_subtitle_alter_category_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 18, 30, 7, 630546, tzinfo=datetime.timezone.utc), verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 18, 30, 7, 631061, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='PB', max_length=2),
        ),
    ]
