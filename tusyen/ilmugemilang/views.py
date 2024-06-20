import datetime
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from ilmugemilang.models import Student,Teacher,Contact,Subject,Class,AssignClass,Payment,Attendance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as auth_logout
from django.db import IntegrityError
from datetime import datetime,date 

# Create your views here.
def usersignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return HttpResponse("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        
        if User.objects.filter(email=useremail).exists():
            return HttpResponse("Email already exists.")
        
        user = User.objects.create_user(username=username, email=useremail, password=password1)
        login(request, user)
        return redirect('userlogin')
    return render(request, 'signup.html')
 

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('mainpage') 
        else:
            return HttpResponse("Invalid login credentials.")

    return render(request, 'userlogin.html')


#=================================================================================================
#teacher signup login
def teachersignup(request):
    if request.method == 'POST':
        username = request.POST.get('staff_username')
        password1 = request.POST.get('staff_password1')
        password2 = request.POST.get('staff_password2')
        
        if password1 != password2:
            return HttpResponse("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        
        teacher = User.objects.create_user(username=username, password=password1)
        login(request, teacher)
        return redirect('teacherlogin')
    return render(request, 'teachersignup.html')


def teacherlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('teacher') 
        else:
            return HttpResponse("Invalid login credentials.")

    return render(request, 'login.html')


#===========================================================================================================
#admin login
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('admin')  
        else:
            return HttpResponse("Username or password is incorrect")
    else:
        return render(request, "adminlogin.html")

def user_logout(request):
    auth_logout(request)  
    return redirect('index')


#=====================================================================================
#user page
def index(request):
    return render(request,'userpage.html')

def mainpage(request):
    return render(request,'userpage2.html')

def mainpage2(request):
    studname = request.GET.get('studname') 
    if studname:
        student = get_object_or_404(Student, studname=studname)
        return render(request, 'userpage3.html', {'student': student})
    else:
        return render(request, 'userpage3.html', {'message': 'Student name not provided'})

def register(request):
    if request.method == 'POST':
        studname = request.POST['name']
        studic = request.POST['nric']
        studage = request.POST['age']
        housenum = request.POST['contact_house']
        mobilenum = request.POST['contact_mobile']
        parentsnum = request.POST['contact_parents']
        houseaddress = request.POST['address']
        email = request.POST['email']
        currentschool = request.POST['school']
        standard = request.POST['standard']
        subject_names = request.POST.getlist('subjects')
        subjects = [Subject.objects.get_or_create(name=name)[0] for name in subject_names]
        
        try:
            data = Student.objects.create(
                studname=studname,
                studic=studic,
                studage=studage,
                housenum=housenum,
                mobilenum=mobilenum,
                parentsnum=parentsnum,
                houseaddress=houseaddress,
                email=email,
                currentschool=currentschool,
                standard=standard,
            )
            data.subjects.set(subjects)  
            return redirect('viewregister', studname=studname)
        except IntegrityError:
            error_message = "A student with the same name already exists. Please choose a different name."
            subjects = Subject.objects.all()
            return render(request, "register.html", {'subjects': subjects, 'error_message': error_message})
    else:
        subjects = Subject.objects.all()
        return render(request, "register.html", {'subjects': subjects}) 
  

def viewregister(request, studname):
    student = get_object_or_404(Student, studname=studname)
    context = {'student': student,}
    return render(request, 'viewregister.html', context)


def updateregister(request, studname):
    student = get_object_or_404(Student, studname=studname)
    if request.method == 'POST':
        student.studname = request.POST['name']
        student.studic = request.POST['nric']
        student.studage = request.POST['age']
        student.housenum = request.POST['contact_house']
        student.mobilenum = request.POST['contact_mobile']
        student.parentsnum = request.POST['contact_parents']
        student.houseaddress = request.POST['address']
        student.email = request.POST['email']
        student.currentschool = request.POST['school']
        student.standard = request.POST['standard']
        student.subjects.clear()  
        
        subject_names = request.POST.getlist('subjects')
        subjects = [Subject.objects.get_or_create(name=name)[0] for name in subject_names]
        student.subjects.add(*subjects) 
        student.save()
        return redirect('viewregister', studname=student.studname)
    
    context = {'student': student,}
    return render(request, 'updateregister.html', context)


def program(request):
    return render(request,'course.html')


def fee(request):
    return render(request,'userpayment.html')


def contact(request):
    if request.method == 'POST':
        #contact_id = request.POST['contact_id']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        data = Contact(name=name, email=email, subject=subject, message=message)
        data.save()

        return redirect(contact)
    else:
        return render(request,"contact.html")



#==================================================================================
#teacher page
def teacher(request):
    if request.method == 'GET' and 'class' in request.GET:
        studclass = request.GET.get('class')
        try:
            class_obj = Class.objects.get(studclass=studclass)
            return redirect('attendance_form', class_id=class_obj.pk)
        except Class.DoesNotExist:
            classes = Class.objects.all()
            return render(request, 'teacherpage.html', {'classes': classes, 'error': 'Class not found'})
    
    classes = Class.objects.all()
    return render(request, 'teacherpage.html', {'classes': classes})


def attendance_form(request, class_id):
    class_assigned = get_object_or_404(Class, pk=class_id)
    students_in_class = AssignClass.objects.filter(class_assigned=class_assigned)
    if request.method == 'POST':
        for assign in students_in_class:
            student = assign.student
            status = request.POST.get(f'status_{student.studname}')
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                class_assigned=class_assigned,
                date=date.today(),
                defaults={'status': status}
            )
            if not created:
                attendance.status = status
                attendance.save()
        return redirect('viewattendance', class_id=class_id)
    context = {
        'class_assigned': class_assigned,
        'students_in_class': students_in_class,
        'date': date.today()
    }
    return render(request, 'attendanceform.html', context)


def viewattendance(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    attendances = Attendance.objects.filter(class_assigned=class_obj)
    context = {
        'class_obj': class_obj,
        'attendances': attendances
    }
    return render(request, 'attendanceview.html', context)



#==================================================================================
#admin page
def admin(request):
    return render(request,'adminpage.html')


def managestudent(request):
    students = Student.objects.all()
    context = {'students': students,}
    return render(request, 'managestud.html', context)


def deletestudent(request, studname):
    student = get_object_or_404(Student, studname=studname)
    if request.method == 'POST':
        student.delete()
        return redirect('managestudent')
    return render(request, 'managestud.html', {'student': student})


def updatestudent(request, student_id):
    student = get_object_or_404(Student, studname=student_id)
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        class_id = request.POST.get('class')
        try:
            selected_subject = Subject.objects.get(id=subject_id)
            selected_class = Class.objects.get(studclass=class_id)
            student.subjects.clear()
            student.subjects.add(selected_subject)
            assign_class, created = AssignClass.objects.update_or_create(
                student=student,
                subject=selected_subject,
                defaults={'class_assigned': selected_class}
            )
            student.standard = selected_class.studclass
            student.save()
            return redirect('managestudent')
        except Subject.DoesNotExist:
            return HttpResponseNotFound("Subject not found")
        except Class.DoesNotExist:
            return HttpResponseNotFound("Class not found")
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'studentupdate.html', {'student': student, 'subjects': subjects, 'classes': classes})


def manageclass(request):
    if request.method == 'POST':
        class_id = request.POST.get('delete_class')
        if class_id:
            class_instance = get_object_or_404(Class, studclass=class_id)
            class_instance.delete()
            return redirect('manageclass')
        studclass = request.POST.get('studclass')
        subject = request.POST.get('subject')
        teachername = request.POST.get('teachername')
        new_class = Class(studclass=studclass, subject=subject, teachername=teachername)
        new_class.save()
        return redirect('manageclass')
    classes = Class.objects.all()
    return render(request, 'manageclass.html', {'classes': classes})


def managepayment(request):
    student = None
    payments = []

    if request.method == "POST":
        if 'search' in request.POST:
            studname = request.POST.get('studname')
            try:
                student = Student.objects.get(studname=studname)
                payments = Payment.objects.filter(student=student)
            except Student.DoesNotExist:
                messages.error(request, "No student matches the given name.")
                return redirect('managepayment')
        elif 'save' in request.POST:
            studname = request.POST.get('studname')
            student = get_object_or_404(Student, studname=studname)
            
            payment_items = [
                ('Registration', 100),
                ('Material Fees', 380),
                ('Misc Fees', 380),
                ('Activities Fees', 380),
                ('Insurance', 380),
                ('Deposit', 350),
            ]

            for item, amount in payment_items:
                payment_status = request.POST.get(item)
                payment_date_str = request.POST.get(f"{item}_date")
                payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date() if payment_date_str else None
                reference_number = request.POST.get(f"{item}_ref", "")

                # Validate payment status
                if not payment_status:
                    messages.error(request, f"Payment status for {item} is required.")
                    return redirect('managepayment')

                Payment.objects.update_or_create(
                    student=student,
                    item=item,
                    defaults={
                        'amount': amount,
                        'paymentstatus': payment_status,
                        'payment_date': payment_date,
                        'reference_number': reference_number,
                    }
                )

            messages.success(request, "Payment information has been updated successfully.")
            return redirect('viewpayment')

    return render(request, 'managepayment.html', {
        'student': student,
        'payments': payments,
    })

def viewpayment(request):
    student = None
    payments = []

    if request.method == "POST":
        studname = request.POST.get('studname')
        try:
            student = Student.objects.get(studname=studname)
            payments = Payment.objects.filter(student=student)
        except Student.DoesNotExist:
            messages.error(request, "No student matches the given name.")
            return redirect('viewpayment')

    return render(request, 'viewpayment.html', {
        'student': student,
        'payments': payments,
    })
