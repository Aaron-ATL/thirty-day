# Generated by Django 5.1.3 on 2024-11-22 00:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='question',
            field=models.CharField(default='Question', max_length=255),
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('answer_1', models.CharField(max_length=255)),
                ('answer_2', models.CharField(max_length=255)),
                ('answer_3', models.CharField(max_length=255)),
                ('correct_answer', models.IntegerField()),
                ('audio_file', models.CharField(max_length=30)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='main_app.quiz')),
            ],
        ),
        migrations.DeleteModel(
            name='QuizAnswer',
        ),
    ]