from .models import Student, StudentInfo, ContactDetails

from rest_framework import serializers

class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = ('contact',)

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ('class_no', 'grad_or_student', 'year', 'dropout')
		
class StudentSerializer(serializers.ModelSerializer):

    contact_details = ContactDetailsSerializer(many=True)
     
    student_info = StudentInfoSerializer(many=True)
    class Meta:
        model = Student
        fields = ('student_id', 'name', 'id_no', 'deceased', 'image_path', 'contact_details', 'student_info')
    
    def create(self, validated_data):
        contact_details_data = validated_data.pop('contact_details')
        student_info_data = validated_data.pop('student_info')
        student = Student.objects.create(**validated_data)
        for contact_detail_data in contact_details_data:
            ContactDetails.objects.create(student=student, **contact_detail_data)
        for info_data in student_info_data:
            StudentInfo.objects.create(student=student, **info_data)
        return student
