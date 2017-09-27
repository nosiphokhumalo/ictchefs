from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Max

from .models import Student, StudentInfo
from django.http import Http404

from adminapp.serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class MenuPageView(TemplateView):
    template_name = "menu.html"

class AddPageView(TemplateView):
    template_name = "addStudents.html"
    
    def get(self, request, **kwargs):
        try:	
            classes = StudentInfo.objects.all().aggregate(Max('class_no'))
        except (Student.DoesNotExist) as e:
            raise Http404('StudentInfo does not exist')
        return render(request, self.template_name,
                      {'classes': classes})

class StatisticsPageView(TemplateView):

    template_name = 'statistics.html'
	
    def get(self, request, **kwargs):
        try:	
            students = Student.objects.all()
            all_students = students.count()
            deceased = students.filter(deceased=1).count()
            graduates = students.filter(student_info__grad_or_student='grad').count()
            dropouts = students.filter(student_info__dropout=1).count()
            employed = students.filter(employment_info__current_employment__isnull=False).count()
            unemployed = students.filter(employment_info__current_employment__isnull=True).count()
            classes = StudentInfo.objects.all().aggregate(Max('class_no'))
        except (Student.DoesNotExist) as e:
            raise Http404('Student does not exist')
        return render(request, self.template_name,
                      {'all_students': all_students, 'deceased': deceased, 'graduates': graduates, 'dropouts': dropouts, 'employed': employed, 'unemployed': unemployed, 'classes': classes})

			
def filter(request):
    yearstart = request.POST.get('yearstart') 
    yearend = request.POST.get('yearend')
    classstart = request.POST.get('classstart')
    classend = request.POST.get('classend')
    if (yearstart and yearend) is not None:
        students = Student.objects.filter(student_info__year__range=(yearstart, yearend))
    elif (classstart and classend) is not None:
    	students = Student.objects.filter(student_info__class_no__range=(classstart, classend))
    data = {'all_students': students.count(), 'deceased': students.filter(deceased=1).count(), 'graduates': students.filter(student_info__grad_or_student='grad').count(), 'dropouts': students.filter(student_info__dropout=1).count(), 'employed': students.filter(employment_info__current_employment__isnull=False).count(), 'unemployed': students.filter(employment_info__current_employment__isnull=True).count()}
    return render(request, 'table.html', data)
    


class StudentList(APIView):
    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

