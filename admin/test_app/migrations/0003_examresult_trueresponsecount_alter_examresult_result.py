# Generated by Django 4.2.13 on 2024-06-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_alter_examresult_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='trueResponseCount',
            field=models.PositiveIntegerField(default=1, verbose_name="To'g'ri yechgan savollar soni"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='examresult',
            name='result',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Natijasi (%)'),
        ),
    ]