# Generated by Django 2.2.12 on 2020-04-27 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InnovzaApp', '0012_auto_20200425_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
