# Generated by Django 5.1.1 on 2024-10-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_formation_dure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscrie',
            name='dates',
            field=models.DateField(auto_now_add=True),
        ),
    ]
