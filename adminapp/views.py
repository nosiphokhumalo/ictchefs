from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Max

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import Student, StudentInfo, ContactDetails, EmploymentInfo, EmploymentHistory, WeekendPlacement
from django.http import Http404

from django.contrib import messages

from adminapp.serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
                if user.is_superuser:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "You are now logged in.")
                    return redirect('/menu/')
                else:
                    return HttpResponse("Your account doesn't have access to this page. To proceed, please login with an account that has access.")
            else:
            	messages.add_message(request, messages.ERROR, "Your account is disabled. To proceed, please login with an account that is active.")
            	return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, "Your username and password didn't match. Please try again.")
            return redirect('/')

    # The request is not a HTTP POST, so display the login form.
    else:
        return render(request, 'index.html', context)

# login_required() decorator to ensure only those logged in can access the view.
@login_required(login_url='/login/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    messages.add_message(request, messages.INFO, "You have been logged out.")
    # Take the user back to the homepage.
    return redirect('/')


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
            years = StudentInfo.objects.all().aggregate(Max('year'))
        except (Student.DoesNotExist) as e:
            raise Http404('Student does not exist')
        return render(request, self.template_name,
                      {'all_students': all_students, 'deceased': deceased, 'graduates': graduates, 'dropouts': dropouts, 'employed': employed, 'unemployed': unemployed, 'classes': classes, 'years': years})

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

def handle_uploaded_file(file, filename):
	with open('static/' + filename, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)



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
            messages.add_message(request._request, messages.INFO, "Student is already in database")
        except Student.DoesNotExist:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse('An error occured')

# Deals with incoming post requests
def postRequestMethod(request):
	if request.method == 'POST':
		# file uploads
		try:
			handle_uploaded_file(request.FILES['image'], str(request.FILES['image']))
		# database edits
		except:
			s_id = request.POST.get('s_id')
			column = request.POST.get('column')
			newValue = request.POST.get('newValue')
			oldValue = request.POST.get('oldValue')

			if (column == "name"):
				student = Student.objects.get(student_id = s_id)
				student.name = newValue
				student.save()
			elif (column == "contact"):
				newArray = newValue.split(",")
				try:
					student = ContactDetails.objects.filter(student=Student.objects.get(student_id=s_id))
					for s in student:
						s.delete()

					s = Student.objects.get(student_id=s_id)
					for i in newArray:
						student = ContactDetails(student=Student.objects.get(student_id=s_id),contact=i)
						student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = ContactDetails(student=Student.objects.get(student_id=s_id),contact=newValue)
					student.save()

			elif (column == "idNumber"):
				student = Student.objects.get(student_id=s_id)
				student.id_no = newValue
				student.save()
			elif (column == "classNumber"):
				try:
					student = StudentInfo.objects.get(student=Student.objects.get(student_id=s_id))
					student.class_no = newValue
					student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = StudentInfo(student=Student.objects.get(student_id=s_id),class_no=newValue,grad_or_student='student',dropout='0')
					student.save()
			elif (column == "year"):
				try:
					student = StudentInfo.objects.get(student=Student.objects.get(student_id=s_id))
					student.year = newValue
					student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = StudentInfo(student=Student.objects.get(student_id=s_id),year=newValue,grad_or_student='student',dropout='0')
					student.save()
			elif (column == "weekend"):
				newArray = newValue.split(",")
				try:
					student = WeekendPlacement.objects.filter(student=Student.objects.get(student_id=s_id))
					for s in student:
						s.delete()

					s = Student.objects.get(student_id=s_id)
					for i in newArray:
						student = WeekendPlacement(student=Student.objects.get(student_id=s_id),placement=i)
						student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = WeekendPlacement(student=Student.objects.get(student_id=s_id),placement=newValue)
					student.save()
			elif (column == "internship"):
				try:
					student = EmploymentInfo.objects.get(student=Student.objects.get(student_id=s_id))
					student.internship = newValue
					student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = EmploymentInfo(student=Student.objects.get(student_id=s_id),internship=newValue)
					student.save()
			elif (column == "current"):
					try:
						student = EmploymentInfo.objects.get(student=Student.objects.get(student_id=s_id))
						student.current_employment = newValue
						student.save()
						if oldValue != "":
							student1 = EmploymentHistory(student=Student.objects.get(student_id=s_id),employment=oldValue)
							student1.save()
					except:
						s = Student.objects.get(student_id=s_id)
						student = EmploymentInfo(student=Student.objects.get(student_id=s_id),current_employment=newValue)
						student.save()
			elif (column == "history"):
				newArray = newValue.split(",")
				try:
					student = EmploymentHistory.objects.filter(student=Student.objects.get(student_id=s_id))
					for s in student:
						s.delete()

					s = Student.objects.get(student_id=s_id)
					for i in newArray:
						student = EmploymentHistory(student=Student.objects.get(student_id=s_id),employment=i)
						student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = EmploymentHistory(student=Student.objects.get(student_id=s_id),employment=newValue)
					student.save()
			elif (column == "status"):
				try:
					student = StudentInfo.objects.get(student=Student.objects.get(student_id=s_id))
					student.grad_or_student = newValue
					if(str(newValue).lower() == "dropout"):
						student.dropout = "1"
					else:
						student.dropout = "0"
					student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = StudentInfo(student=Student.objects.get(student_id=s_id),grad_or_student=newValue,dropout='0')
					student.save()
			elif (column == "dropout"):
				try:
					student = StudentInfo.objects.get(student=Student.objects.get(student_id=s_id))
					student.dropout = newValue
					if (str(newValue) == "1"):
						student.grad_or_student = "dropout"
					student.save()
				except:
					s = Student.objects.get(student_id=s_id)
					student = StudentInfo(student=Student.objects.get(student_id=s_id),dropout=newValue)
					student.save()
			elif (column == "deceased"):
				student = Student.objects.get(student_id=s_id)
				student.deceased = newValue
				student.save()
			elif (column == "appActive"):
				student = Student.objects.filter(student_id=s_id)
			elif (column == "image_path"):
				print(newValue)
				student = Student.objects.get(student_id=s_id)
				student.image_path = newValue
				student.save()
			elif (column == "file_path"):
				print(newValue)
				student = Student.objects.get(student_id=s_id)
				student.file_path = newValue
				student.save()
			elif (column == "delete"):
				student = Student.objects.get(student_id=s_id)
				student.delete()

# pull student record from the database and create json string
def getStudents(students):
	rows = ''
	for s in students:
		rows += '{"s_id":"' + str(s.student.student_id) + '",'
		theStudent = Student.objects.get(student_id=s.student.student_id)
		if (theStudent.name is None ):
			rows += '"name":"",'
		else:
			rows += '"name":"' +theStudent.name + '",'

		if (theStudent.id_no is None ):
			rows += '"idNumber":"",'
		else:
			rows += '"idNumber":"' + theStudent.id_no + '",'
		if (theStudent.image_path is None ):
			rows += '"imagePath":"",'
		else:
			rows += '"imagePath":"' + theStudent.image_path + '",'
		if (theStudent.file_path is None ):
			rows += '"filePath":"",'
		else:
			rows += '"filePath":"' + theStudent.file_path + '",'

		rows += '"deceased":"' + str(theStudent.deceased) + '",'

		history = EmploymentHistory.objects.filter(student=s.student)
		temp = ''
		for h in history:
			h = h.employment
			h = h.replace("'","’")
			h = h.replace('"','')
			h = " " + h
			temp += '"' + h + '", '
		temp = temp [:-1]
		temp = temp [:-1]
		if (len(temp) == 0):
			rows += '"history":"",'
		else:
			temp = '[' + temp + ']'
			rows += '"history":'+ temp +','

		try:
			current = str(EmploymentInfo.objects.get(student=s.student).current_employment)
			current = current.replace("'","’")
			rows += '"current":"'+ current +'",'
		except:
			rows += '"current":"",'

		try:
			placement = str(EmploymentInfo.objects.get(student=s.student).internship)
			placement = placement.replace("'","’")
			rows += '"internship":"'+ placement +'",'
		except:
			rows += '"internship":"",'

		placement = WeekendPlacement.objects.filter(student=s.student)
		temp = ''
		for w in placement:
			w = w.placement
			w = w.replace("'","’")
			w = " " + w
			temp += '"' + w + '", '
		temp = temp [:-1]
		temp = temp [:-1]

		if (len(temp) == 0):
			rows += '"weekend":"",'
		else:
			temp = '[' + temp + ']'
			rows += '"weekend":'+ temp +','

		try:
			rows += '"classNumber":"'+str(StudentInfo.objects.get(student=s.student).class_no)+'",'
		except:
			rows += '"classNumber":"",'

		try:
			rows += '"year":"'+str(StudentInfo.objects.get(student=s.student).year)+'",'
		except:
			rows += '"year":"",'

		contact = ContactDetails.objects.filter(student=s.student)
		temp = ''
		for c in contact:
			c = c.contact
			c = " " + c
			temp += '"' + c + '", '
		temp = temp [:-1]
		temp = temp [:-1]

		if (len(temp) == 0):
			rows += '"contact":"",'
		else:
			temp = '[' + temp + ']'
			rows += '"contact":'+ temp +','

		try:
			rows += '"status":"'+str(StudentInfo.objects.get(student=s.student).grad_or_student)+'",'
		except:
			rows += '"status":"",'

		try:
			rows += '"dropout":"'+str(StudentInfo.objects.get(student=s.student).dropout)+'"'
		except:
			rows += '"dropout":""'

		rows += '},'

	rows = rows[:-1]
	return rows

# view students view, pulls all records from the database that are current students and sends it to the front-end
@login_required(login_url='/login/')
def viewStudent(request):
	postRequestMethod(request)

	students = StudentInfo.objects.filter(grad_or_student="student")

	rows = getStudents(students)

	return render(request, "viewStudents.html", {'sInfo':rows})

# view graduates view, pulls all records from the database that are graduates and sends it to the front-end
@login_required(login_url='/login/')
def viewGraduate(request):
	postRequestMethod(request)

	students = StudentInfo.objects.filter(grad_or_student="grad")

	rows = getStudents(students)

	return render(request, "viewGraduates.html", {'sInfo':rows})

# view dropouts view, pulls all records from the database that are dropouts and sends it to the front-end
@login_required(login_url='/login/')
def viewDropout(request):
	postRequestMethod(request)

	students = StudentInfo.objects.filter(grad_or_student="dropout")

	rows = getStudents(students)

	return render(request, "viewDropouts.html", {'sInfo':rows})
