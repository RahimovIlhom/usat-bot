# Generated by Django 4.2.13 on 2024-05-31 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionsCount', models.IntegerField()),
                ('language', models.CharField(choices=[('uz', 'Uzbek'), ('ru', 'Russian')], max_length=2)),
                ('isActive', models.BooleanField(default=False)),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('science', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tests', to='users.science')),
            ],
            options={
                'db_table': 'tests',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('question', models.TextField()),
                ('trueResponse', models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=1)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='test_app.test')),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.DecimalField(decimal_places=2, max_digits=5)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_result', to='users.applicant')),
            ],
            options={
                'db_table': 'exam_results',
            },
        ),
    ]
