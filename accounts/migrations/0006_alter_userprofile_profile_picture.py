# Generated by Django 4.1.5 on 2023-02-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=255, upload_to='userprofile'),
        ),
    ]
