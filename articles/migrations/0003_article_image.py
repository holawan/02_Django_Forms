# Generated by Django 3.2.12 on 2022-04-08 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20220308_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
