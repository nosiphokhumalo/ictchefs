from .models import Student, StudentInfo, EmploymentInfo
from django.contrib.auth.models import User
from django import forms
from rest_framework import serializers

class EmploymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentInfo
        fields = ('internship', 'current_employment')

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ('class_no', 'grad_or_student', 'year', 'dropout')

class UserSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all())

    class Meta:
        model = User

        fields = ('id', 'username', 'students')

class AppSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    contact_details = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='contact'
     )
     
    employment_history = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='employment'
     )
     
    employment_info = EmploymentInfoSerializer(many=True, read_only=True)
    
    weekend_placement = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='placement'
     )
     
    student_info = StudentInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = ('student_id','owner','activated', 'password', 'name', 'id_no', 'deceased', 'contact_details','address' ,'employment_history', 'employment_info', 'weekend_placement', 'student_info')
    def create(self, validated_data):
        contact_details_data = validated_data.pop('contact_details')
        student_info_data = validated_data.pop('student_info')
        student = Student.objects.create(**validated_data)
        for contact_detail_data in contact_details_data:
            ContactDetails.objects.create(student=student, **contact_detail_data)
        for info_data in student_info_data:
            StudentInfo.objects.create(student=student, **info_data)
        return student
