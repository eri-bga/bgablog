# Generated by Django 4.1.5 on 2023-01-18 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profession',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
