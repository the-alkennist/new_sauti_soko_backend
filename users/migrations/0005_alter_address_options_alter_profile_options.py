# Generated by Django 4.0.4 on 2024-03-08 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_address_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-created_at',)},
        ),
    ]
