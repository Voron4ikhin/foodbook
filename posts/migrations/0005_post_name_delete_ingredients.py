# Generated by Django 4.0.4 on 2022-05-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_rename_ingredients_post_components_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.DeleteModel(
            name='Ingredients',
        ),
    ]
