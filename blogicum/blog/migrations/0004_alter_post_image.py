# Generated by Django 3.2.16 on 2023-11-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20231108_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images', verbose_name='Фото'),
        ),
    ]