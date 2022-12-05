# Generated by Django 4.1.3 on 2022-12-05 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='courses',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='sections',
        ),
        migrations.CreateModel(
            name='AssignedClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.section')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teacher')),
            ],
        ),
    ]
