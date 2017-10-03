# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'db_table': 'contact_details',
            },
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'employment_history',
            },
        ),
        migrations.CreateModel(
            name='EmploymentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('internship', models.CharField(max_length=50, null=True, blank=True)),
                ('current_employment', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'employment_info',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('id_no', models.CharField(max_length=50, null=True, blank=True)),
                ('deceased', models.IntegerField(null=True, blank=True)),
                ('image_path', models.CharField(max_length=100, null=True, blank=True)),
                ('file_path', models.CharField(max_length=100, null=True, blank=True)),
                ('password', models.CharField(max_length=50, null=True, default='', blank=True)),
                ('activated', models.IntegerField(null=True, default=0, blank=True)),
                ('address', models.CharField(max_length=50, null=True, default='South Africa', blank=True)),
                ('user', models.ForeignKey(default=1, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('class_no', models.IntegerField(null=True, blank=True)),
                ('grad_or_student', models.CharField(max_length=10, null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('dropout', models.IntegerField(null=True, blank=True)),
                ('student', models.ForeignKey(related_name='student_info', db_column='student_id', to='adminapp.Student')),
            ],
            options={
                'db_table': 'student_info',
            },
        ),
        migrations.CreateModel(
            name='WeekendPlacement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('placement', models.CharField(max_length=100, null=True, blank=True)),
                ('student', models.ForeignKey(related_name='weekend_placement', db_column='student_id', to='adminapp.Student')),
            ],
            options={
                'db_table': 'weekend_placement',
            },
        ),
        migrations.AddField(
            model_name='employmentinfo',
            name='student',
            field=models.ForeignKey(related_name='employment_info', db_column='student_id', to='adminapp.Student'),
        ),
        migrations.AddField(
            model_name='employmenthistory',
            name='student',
            field=models.ForeignKey(related_name='employment_history', db_column='student_id', to='adminapp.Student'),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='student',
            field=models.ForeignKey(related_name='contact_details', db_column='student_id', to='adminapp.Student'),
        ),
    ]
