# Generated by Django 4.1.5 on 2023-01-19 21:39

import blog.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_category_image_post_image_alter_category_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default/no_image.jpg', max_length=255, upload_to=blog.models.Category.image_upload_to),
        ),
        migrations.AlterField(
            model_name='category',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 19, 21, 39, 13, 956817, tzinfo=datetime.timezone.utc), verbose_name='Date Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default/no_image.jpg', max_length=255, upload_to=blog.models.Post.image_upload_to),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 19, 21, 39, 13, 958124, tzinfo=datetime.timezone.utc)),
        ),
    ]
