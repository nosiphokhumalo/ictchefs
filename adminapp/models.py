from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    id_no = models.CharField(max_length=50, blank=True, null=True)
    deceased = models.IntegerField(blank=True, null=True, default=0)
    image_path = models.CharField(max_length=100, blank=True, null=True, default=None)
    file_path = models.CharField(max_length=100, blank=True, null=True, default=None)
    user = models.ForeignKey(User, related_name='student', default=1, on_delete=models.DO_NOTHING)
    password = models.CharField(max_length=50, default=None, blank=True, null=True)
    activated = models.IntegerField(default=0, blank=True, null=True)
    address = models.CharField(default='South Africa', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'student'


class ContactDetails(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column='student_id', related_name='contact_details',on_delete=models.CASCADE)
    contact = models.CharField(max_length=30,  blank=True, null=True)

    class Meta:
        db_table = 'contact_details'



class EmploymentHistory(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column='student_id', related_name='employment_history', on_delete=models.CASCADE)
    employment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'employment_history'



class EmploymentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column='student_id', related_name='employment_info', on_delete=models.CASCADE)
    internship = models.CharField(max_length=50, blank=True, null=True)
    current_employment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'employment_info'



class StudentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column='student_id', related_name='student_info', on_delete=models.CASCADE)
    class_no = models.IntegerField(blank=True, null=True)
    grad_or_student = models.CharField(max_length=10, blank=True, null=True, default='student')
    year = models.IntegerField(blank=True, null=True)
    dropout = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'student_info'




class WeekendPlacement(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, db_column='student_id', related_name='weekend_placement', on_delete=models.CASCADE)
    placement = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'weekend_placement'
