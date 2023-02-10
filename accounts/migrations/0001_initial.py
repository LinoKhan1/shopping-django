# Generated by Django 4.1.5 on 2023-02-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=201)),
                ('last_name', models.CharField(max_length=201)),
                ('username', models.CharField(max_length=201, unique=True)),
                ('email', models.EmailField(max_length=201, unique=True)),
                ('phone_number', models.CharField(max_length=201)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_join', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
