# Generated by Django 5.0.6 on 2024-07-05 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_remove_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='BlogCover',
            field=models.ImageField(blank=True, null=True, upload_to='post_images'),
        ),
    ]
