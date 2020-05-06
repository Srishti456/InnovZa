# Generated by Django 2.2.12 on 2020-05-02 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InnovzaApp', '0020_auto_20200502_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InnovzaApp.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InnovzaApp.UserInfo')),
            ],
        ),
    ]
