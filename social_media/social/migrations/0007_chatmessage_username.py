# Generated by Django 4.0 on 2023-02-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='username',
            field=models.CharField(default='admin', max_length=255),
            preserve_default=False,
        ),
    ]