# Generated by Django 5.0.6 on 2024-08-12 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0019_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
