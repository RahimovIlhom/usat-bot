# Generated by Django 4.2.13 on 2024-07-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_olympian_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='passportImageBack',
            field=models.ImageField(blank=True, null=True, upload_to='passport/images/back/', verbose_name='Pasport orqa rasmi'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='passportImageFront',
            field=models.ImageField(blank=True, null=True, upload_to='passport/images/front/', verbose_name='Pasport old rasmi'),
        ),
    ]
