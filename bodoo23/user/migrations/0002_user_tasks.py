# Generated by Django 3.2.15 on 2022-09-26 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_taskuserrel'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tasks',
            field=models.ManyToManyField(through='tasks.TaskUserRel', to='tasks.Task'),
        ),
    ]
