# Generated by Django 4.2.16 on 2024-10-16 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('oneplate', '0003_Like_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='content_type',
            new_name='content_type_id',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'content_type_id', 'object_id')},
        ),
    ]
