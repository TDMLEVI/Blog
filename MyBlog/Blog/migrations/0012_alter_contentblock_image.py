# Generated by Django 5.0.6 on 2024-07-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0011_post_trending_post_views_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblock',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
