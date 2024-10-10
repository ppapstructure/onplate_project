# Generated by Django 4.2.16 on 2024-10-10 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneplate', '0002_User_name_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
