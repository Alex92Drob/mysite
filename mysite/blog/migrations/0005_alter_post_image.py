# Generated by Django 5.0.7 on 2024-08-11 10:43

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to=blog.models.user_directory_path),
        ),
    ]
