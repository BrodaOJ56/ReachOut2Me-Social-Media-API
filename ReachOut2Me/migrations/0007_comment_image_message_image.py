# Generated by Django 4.2 on 2023-04-15 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReachOut2Me', '0006_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='comment_images/'),
        ),
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message_images/'),
        ),
    ]
