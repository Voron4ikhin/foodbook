# Generated by Django 4.0.4 on 2022-05-25 21:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_name_delete_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]
