# Generated by Django 4.1.3 on 2022-12-02 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_student_sem_student_sem'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
