# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('contact', models.CharField(null=True, blank=True, max_length=30)),
            ],
            options={
                'db_table': 'contact_details',
            },
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('employment', models.CharField(null=True, blank=True, max_length=1000)),
            ],
            options={
                'db_table': 'employment_history',
            },
        ),
        migrations.CreateModel(
            name='EmploymentInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('internship', models.CharField(null=True, blank=True, max_length=50)),
                ('current_employment', models.CharField(null=True, blank=True, max_length=1000)),
            ],
            options={
                'db_table': 'employment_info',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(null=True, blank=True, max_length=50)),
                ('id_no', models.CharField(null=True, blank=True, max_length=50)),
                ('deceased', models.IntegerField(null=True, blank=True)),
                ('image_path', models.CharField(null=True, blank=True, max_length=100)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('class_no', models.IntegerField(null=True, blank=True)),
                ('grad_or_student', models.CharField(null=True, blank=True, max_length=10)),
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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('placement', models.CharField(null=True, blank=True, max_length=100)),
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
