# Generated by Django 3.0.8 on 2020-08-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_like_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='liked',
        ),
        migrations.AlterField(
            model_name='like',
            name='post',
            field=models.IntegerField(),
        ),
    ]
