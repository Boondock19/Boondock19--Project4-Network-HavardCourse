# Generated by Django 3.1.3 on 2020-12-07 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Follower', models.ManyToManyField(blank=True, related_name='User_Follower', to=settings.AUTH_USER_MODEL)),
                ('Following', models.ManyToManyField(blank=True, related_name='User_Following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_Profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contend', models.CharField(max_length=300)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('like', models.ManyToManyField(blank=True, related_name='Post_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_Post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
