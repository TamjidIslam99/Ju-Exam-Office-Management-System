# Generated by Django 5.0.6 on 2024-10-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_Office', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]