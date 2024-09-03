# Generated by Django 5.0.4 on 2024-04-19 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='Body_1',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_2',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_3',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_4',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_5',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_6',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_7',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_8',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_9',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
        migrations.AddField(
            model_name='post',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
        migrations.AddField(
            model_name='post',
            name='Body_10',
            field=models.TextField(default='Enter the body of your blog here!'),
        ),
    ]
