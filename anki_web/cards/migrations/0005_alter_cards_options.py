# Generated by Django 4.1.4 on 2023-01-03 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_cards_random_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cards',
            options={'ordering': ['random_num']},
        ),
    ]
