# Generated by Django 3.2.8 on 2021-11-14 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_two_factor_face_auth', '0002_auto_20211114_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]