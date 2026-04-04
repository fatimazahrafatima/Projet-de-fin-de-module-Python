# student/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Parent ,ExamResult,Exam,Holiday
from department.models import Department
from datetime import datetime, timedelta
import calendar
def student_dashboard(request):
    # Get logged-in student (adjust if needed)
    student = Student.objects.get(user=request.user)

    # 📚 Courses
    enrolled_courses = student.student_class.count()
    total_courses = 6

    # 📝 Exams
    results = ExamResult.objects.filter(student=student)

    total_tests = results.count()
    tests_attended = results.exclude(status='pending').count()
    tests_passed = results.filter(status='passed').count()

    # 📊 Average grade
    grades = results.exclude(grade=None)
    if grades.exists():
        average_grade = round(sum([r.grade for r in grades]) / grades.count(), 2)
    else:
        average_grade = 0

    # 📅 Learning history (you can improve later)
    learning_history = results.select_related('exam').order_by('-exam__exam_date')[:5]
  
    today = datetime.today()
    year = today.year
    month = today.month

    # Exams and holidays
    exams = Exam.objects.filter(exam_date__year=year, exam_date__month=month)
    exam_days = {e.exam_date.day: e for e in exams}

    holidays = Holiday.objects.filter(
        date_start__lte=datetime(year, month, calendar.monthrange(year, month)[1]),
        date_end__gte=datetime(year, month, 1)
    )

    # Build calendar days
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

    # Split days into weeks (lists of 7)
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
 return render(request, 'students/students.html')
def edit_student(request, student_id):
 return render(request, 'students/edit-student.html')
def view_student(request, student_id):
 return render(request, 'students/student-details.html')
def delete_student(request, student_id):
 return redirect('student_list')
def add_student(request):
 if request.method == 'POST':
 # Récupérer les données de l'étudiant
  first_name = request.POST.get('first_name')
  last_name = request.POST.get('last_name')
  student_id = request.POST.get('student_id')
  gender = request.POST.get('gender')
  date_of_birth = request.POST.get('date_of_birth')
  student_class = request.POST.get('student_class')
  joining_date = request.POST.get('joining_date')
  mobile_number = request.POST.get('mobile_number')
  admission_number = request.POST.get('admission_number')
  section = request.POST.get('section')
  student_image = request.FILES.get('student_image')
  # Récupérer les données du parent
  father_name = request.POST.get('father_name')
  father_occupation = request.POST.get('father_occupation')
  father_mobile = request.POST.get('father_mobile')
  father_email = request.POST.get('father_email')
  mother_name = request.POST.get('mother_name')
  mother_occupation = request.POST.get('mother_occupation')
  mother_mobile = request.POST.get('mother_mobile')
  mother_email = request.POST.get('mother_email')
  present_address = request.POST.get('present_address')
  permanent_address = request.POST.get('permanent_address')
  parent = Parent.objects.create(
   father_name=father_name,
   father_occupation=father_occupation,
   father_mobile=father_mobile,
   father_email=father_email,
   mother_name=mother_name,
   mother_occupation=mother_occupation,
   mother_mobile=mother_mobile,
   mother_email=mother_email,
   present_address=present_address,
   permanent_address=permanent_address
    )
  student = Student.objects.create(
   first_name=first_name,
   last_name=last_name,
   student_id=student_id,
   gender=gender,
   date_of_birth=date_of_birth,
   student_class=student_class,
   joining_date=joining_date,
   mobile_number=mobile_number,
   admission_number=admission_number,
   section=section,
   student_image=student_image,
   parent=parent
   )
  messages.success(request, 'Student added Successfully')
  return redirect('student_list')
 else:
  return render(request, 'students/add-student.html')
 
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
