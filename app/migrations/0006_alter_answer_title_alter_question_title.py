# Generated by Django 4.1.3 on 2022-12-05 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_answer_author_alter_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
