# Generated by Django 2.1.7 on 2020-01-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peoplestory', '0011_stories_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
