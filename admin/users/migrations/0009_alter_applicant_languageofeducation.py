# Generated by Django 4.2.13 on 2024-06-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_applicant_passport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='languageOfEducation',
            field=models.CharField(blank=True, choices=[('uz', 'Uzbek'), ('ru', 'Russian')], default='uz', max_length=2, null=True, verbose_name="Ta'lim tili"),
        ),
    ]