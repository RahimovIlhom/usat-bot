# Generated by Django 4.2.13 on 2024-06-11 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissiontoken',
            name='updatedTime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Token eskirgan vaqt'),
        ),
    ]
