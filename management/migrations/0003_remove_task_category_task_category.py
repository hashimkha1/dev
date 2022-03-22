# Generated by Django 4.0.3 on 2022-03-21 02:37

from django.db import migrations, models
import django.db.models.deletion
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_remove_tag_slug_remove_task_slug_task_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(default=management.models.Tag.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.tag'),
        ),
    ]
