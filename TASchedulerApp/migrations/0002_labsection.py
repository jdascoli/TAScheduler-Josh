# Generated by Django 5.1.2 on 2024-12-09 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TASchedulerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('section', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_sections', to='TASchedulerApp.mycourse')),
                ('instructor', models.ForeignKey(blank=True, limit_choices_to={'role': 'Instructor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_sections', to=settings.AUTH_USER_MODEL)),
                ('ta', models.ForeignKey(blank=True, limit_choices_to={'role': 'TA'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab_sections_ta', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
