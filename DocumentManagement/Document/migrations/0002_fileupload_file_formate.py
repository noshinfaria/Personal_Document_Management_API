# Generated by Django 3.2.5 on 2023-08-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_formate',
            field=models.CharField(default='', max_length=30),
        ),
    ]
