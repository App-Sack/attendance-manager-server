# Generated by Django 4.1.5 on 2023-01-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_student_parent_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="parent_phone_number",
            field=models.CharField(max_length=15),
        ),
    ]
