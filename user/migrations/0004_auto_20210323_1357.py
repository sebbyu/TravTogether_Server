# Generated by Django 3.0.5 on 2021-03-23 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210323_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userPhotoURL',
            field=models.URLField(max_length=254, verbose_name='userPhotoURL'),
        ),
    ]