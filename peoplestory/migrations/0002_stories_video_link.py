# Generated by Django 3.0.1 on 2021-03-13 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peoplestory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='video_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]
