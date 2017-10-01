from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Max

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import Student, StudentInfo
from django.http import Http404

from adminapp.serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/menu/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied. Please try again.")

    # The request is not a HTTP POST, so display the login form.
    else:
        return render(request, 'index.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required(login_url='/login/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

        
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

@login_required(login_url='/login/')			
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
        sname = request.data['name']
        sid_no = request.data['id_no']
        try:
            obj = Student.objects.get(name=sname, id_no=sid_no)
        except Student.DoesNotExist:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse("Student already in database")

        

