# Generated by Django 4.1.1 on 2022-10-12 15:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user', 'project')},
        ),
    ]