# student/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Parent ,ExamResult,Exam
from teacher.models import Teacher
from subject.models import Subject
from holiday.models import Holiday
from department.models import Department
from datetime import datetime, timedelta
from home_auth.models import CustomUser
from django.contrib import messages
import calendar
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    enrolled_courses = student.student_class.count()
    total_courses = 6
    results = ExamResult.objects.filter(student=student)
    total_tests = results.count()
    tests_attended = results.exclude(status='pending').count()
    tests_passed = results.filter(status='passed').count()
    grades = results.exclude(grade=None)
    if grades.exists():
        average_grade = round(sum([r.grade for r in grades]) / grades.count(), 2)
    else:
        average_grade = 0
    learning_history = results.select_related('exam').order_by('-exam__exam_date')[:5]
  
    today = datetime.today()
    year = today.year
    month = today.month
  #calender
    exams = Exam.objects.filter(exam_date__year=year, exam_date__month=month)
    exam_days = {e.exam_date.day: e for e in exams}

    holidays = Holiday.objects.filter(
        date_start__lte=datetime(year, month, calendar.monthrange(year, month)[1]),
        date_end__gte=datetime(year, month, 1)
    )
    cal = calendar.Calendar()
    days = []
    for day in cal.itermonthdays(year, month):
        if day == 0:
            days.append({'day': 0})
            continue

        date_obj = datetime(year, month, day)
        is_weekend = date_obj.weekday() >= 5
        holiday = next((h for h in holidays if h.date_start <= date_obj.date() <= h.date_end), None)
        exam = exam_days.get(day)

        days.append({
            'day': day,
            'is_weekend': is_weekend,
            'holiday': holiday,
            'exam': exam
        })

    weeks = [days[i:i+7] for i in range(0, len(days), 7)]


    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
        'total_courses': total_courses,
        'total_tests': total_tests,
        'tests_attended': tests_attended,
        'tests_passed': tests_passed,
        'average_grade': average_grade,
        'learning_history': learning_history,
        'weeks': weeks,
        'month_name': calendar.month_name[month],
        'year': year
    }



    return render(request, 'students/student-dashboard.html', context)
def student_list(request):
 teacher = Teacher.objects.get(user=request.user)
 subjects = Subject.objects.filter(Teacher=teacher)
 student_list=  Student.objects.filter(student_class__in=subjects).distinct()
 return render(request, 'students/students.html',{'Teacher':  teacher,'student_list' :student_list,})
def edit_student(request, student_id):
 return render(request, 'students/edit-student.html')
def view_student(request, student_id):
 return render(request, 'students/student-details.html')
def delete_student(request, student_id):
 Student.objects.filter(student_id=student_id).delete()
 return redirect('students_teacher')
def add_student(request):

    subjects = Subject.objects.all()

    if request.method == "POST":
        # USER
        username = request.POST.get("email")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_student = True
        user.save()

        # PARENT
        parent = Parent.objects.create(
            father_name=request.POST.get("father_name"),
            father_mobile=request.POST.get("father_mobile"),
            mother_name=request.POST.get("mother_name"),
            mother_mobile=request.POST.get("mother_mobile"),
        )

        # STUDENT
        student = Student.objects.create(
            user=user,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            student_id=request.POST.get("student_id"),
            gender=request.POST.get("gender"),
            date_of_birth=request.POST.get("date_of_birth"),
            joining_date=request.POST.get("joining_date"),
            mobile_number=request.POST.get("mobile_number"),
            admission_number=request.POST.get("admission_number"),
            section=request.POST.get("section"),
            parent=parent,
            student_image=request.FILES.get("student_image")
        )

        # MANY TO MANY
        subjects_selected = request.POST.getlist("student_class")
        student.student_class.set(subjects_selected)
        useroo=request.user
        teacher = Teacher.objects.get(user=request.user)
        messages.success(request, 'student added!')
        return redirect('students_teacher')

    return render(request, 'students/add-student.html', {
    "subjects": subjects
})

 
def departmentsve(request):
  student = Student.objects.get(user=request.user)
  user=request.user
  departments = Department.objects.all()
  context = {'student': student,
             'departments':departments}
  return render(request,'students/departments.html',context)
def Courses_ve(request):
  student = Student.objects.get(user=request.user)
  user=request.user
  Courses = student.student_class.all()
  context = {'student': student,
             'Courses':Courses}
  return render(request,'students/Courses.html',context)
def Exam_ve(request):
  user=request.user
  student = Student.objects.get(user=request.user)
  exams = Exam.objects.filter(subject__in=student.student_class.all())
  context = {'student': student,
             'exams':exams}
  return render(request,'students/Exam.html',context)
def grades_ve(request):
  user=request.user
  student = Student.objects.get(user=request.user)
  exam_results = student.exam_results.select_related('exam', 'exam__subject')

  context = {'student': student,
        'exam_results': exam_results}
  return render(request,'students/grades.html',context)
