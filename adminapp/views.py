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
from adminapp.serializer1 import AppSerializer
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
                    return redirect('/')
                else:
                    return HttpResponse("Your account doesn't have access to this page. To proceed, please login with an account that has access.")
            else:
            	messages.add_message(request, messages.ERROR, "Your account is disabled. To proceed, please login with an account that is active.")
            	return redirect('/login-form/')
        else:
            messages.add_message(request, messages.ERROR, "Your username and password didn't match. Please try again.")
            return redirect('/login-form/')

    # The request is not a HTTP POST, so display the login form.
    else:
        return render(request, 'login.html')

# login_required() decorator to ensure only those logged in can access the view.
@login_required(login_url='/login/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    messages.add_message(request, messages.INFO, "You have been logged out.")
    # Take the user back to the homepage.
    return redirect('/')


class LoginPageView(TemplateView):
    template_name = "login.html"

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
        except Student.DoesNotExist:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Student is in the database
        return Response({'message': 'Student is in database'}, status=status.HTTP_202_ACCEPTED)

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

class StudentManager(APIView):

    """

    Retrieve, update or delete a student instance.

    """



    def get_object(self, pk):

        try:

            return Student.objects.get(pk=pk)

        except Student.DoesNotExist:

            raise Http404

    def get_pk_from_name(self,student_name, student_password):

        try:

            return Student.objects.get(name=student_name,password=student_password)

        except Student.DoesNotExist:

            print("FAM")

            return Response("what are you save")

    def is_student_new(self,student_name):

        num_results = Student.objects.filter(name = student_name).count()

        if(num_results==0):

            return True #the student is new

        else:

            return False #the student exits



    def get(self, request, format=None):

        print(request.data)

        name= request.data.get('name')

        password=request.data.get('password')

        student = self.get_pk_from_name(name,password)

        serial = AppSerializer(student)

        return Response(serial.data)

    def createuser(self,name,password,request):

        student = Student.objects.create()

        student.name=name

        student.password=password

        student.address='South Africa, Western Cape, Cape Town, Khayelisha'

        student.save()

        student.activated=1

        student.id_no=""

        student.deceased=0

        student.save()

        #add the student's profile

        print(' contact details')

        student=ContactDetails(student=self.get_pk_from_name(name,password),contact=request.data.get('contact'))

        student.save()

        student = EmploymentHistory(student=self.get_pk_from_name(name,password),employment="")

        student.save()

        student= StudentInfo(student=self.get_pk_from_name(name,password),grad_or_student='student',year=2017,class_no=0)

        student.save()

        student = WeekendPlacement(student=self.get_pk_from_name(name,password),placement="")

        student.save()

        student = EmploymentInfo(student=self.get_pk_from_name(name,password),current_employment="",internship="")

        student.save()



        return 'Created a new user'





    def post(self, request,format=None):

        print(request.data)

        if(request.data.get('title')=='register'):

            #check if the student is in the db

            name= request.data.get('name')

            password=request.data.get('password')

            if(self.is_student_new(name)):

                self.createuser(name,password,request)

                return Response('Created a new user')

            else:

                print("student is already in the db") #update their concat details and password, then set them to active

                student=Student.objects.get(name=name)

                if(student.activated==0 ):

                    student.activated=1

                    student.save()

                    student.password=password

                    student.save()

                    return Response('activated your account')

                else:

                    return Response('This account already activated')

                #check if their account is active

            return Response("Could not do anything with the user")

        elif request.data.get('title'=='forgot password'):

            print('forgot password')

            try:

                name = request.data.get('name')

                student = Student.objects.get(name = name)

                contact= request.data.get('contact')

                password= student.password

                print(password)

                student = ContactDetails.objects.filter(student=self.get_pk_from_name(name,password))

                for c in student:

                    if (c==contact):

                        return Response('Success _'+password+'_')

                return Response('Unknown User ')

            except:

                return Response('[Student not found]')

        #we are not creating a new user

        name=request.data.get('name') #username and password are now passed as parameters

        password=request.data.get('image') #I like to hide the password



        student=Student.objects.get(name=name,password=password) #get all the info about the student



        #serializer = StudentSerializer(student,data=request.data) #when students edit their data

        #crashes

        if request.data.get('title')=='edit profile':

            print("edit")

            name = request.data.get('new_name')

            contact= request.data.get('contact')

            other_contact=request.data.get('other_contact')

            id_no = request.data.get('id_no')

            classno=request.data.get('class')

            student.name=name

            student.id_no= id_no

            student.save()

            student = ContactDetails.objects.filter(student=self.get_pk_from_name(name,password))

            for c in student:

                 c.delete();

            student=ContactDetails(student=self.get_pk_from_name(name,password),contact=contact)

            student.save()

            student=ContactDetails(student=self.get_pk_from_name(name,password),contact=other_contact)

            student.save()

            student = StudentInfo.objects.get(student=self.get_pk_from_name(name,password))

            student.class_no= int(classno)

            student.save()

            return Response("Edited successfully")



        elif request.data.get('title')=='update address':

            student=Student.objects.get(name=name,password=password)

            address= request.data.get('address')

            student.address=address

            student.save()

            print(request.data.get('address'))

            return Response("Edited the address")



        elif request.data.get('title')=='new job':

            new_job = request.data.get('new job')

            print('new job')

            try:

                student=EmploymentInfo.objects.get(student=self.get_pk_from_name(name,password)) #convert student to list of all employment info

                student.current_employment= new_job

                student.save()

                student= EmploymentHistory(student=self.get_pk_from_name(name,password), employment=new_job)

                student.save()

            except:

                s = self.get_pk_from_name(name,password)

                return Response(" Could not find employent history")

            return Response("You got a new job")

        elif request.data.get('title')=='lost job':

            print('lost job')

            student=EmploymentInfo.objects.get(student=self.get_pk_from_name(name,password)) #convert student to list of all employment info

            student.current_employment = "" #add it as a new employment

            student.save()

            return Response('You have lost your job')

        elif request.data.get('title')=='log in':

            print('logging in -----------------------------------------------------')

            print(request.data)

            serial = AppSerializer(student)

            return Response(serial.data)

        print('UNKNOWN REQUEST :'+request.data.get('title'))

        return Response('UNKNOWN REQUEST :' +request.data.get('title'))



    def delete(self, request, pk, format=None):

        student = self.get_object(pk)

        student.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
