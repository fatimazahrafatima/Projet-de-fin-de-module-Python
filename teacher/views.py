from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher
from student.models import Student,Exam,ExamResult
from subject.models import Subject
from holiday.models import Holiday
from department.models import Department
from django.utils import timezone
from datetime import datetime
import calendar

def dashboard(request):
    Teacherr = Teacher.objects.get(user=request.user)
    subjects = Subject.objects.filter(Teacher=Teacherr)
    students   =  Student.objects.filter(student_class__in=subjects).distinct()
    upcoming_exams= Exam.objects.filter(
        subject__in=subjects,
        exam_date__gt=timezone.now()
    )
    papers_To_Grade= ExamResult.objects.filter(
        exam__subject__in=subjects,
        status='pending'
    )
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

    # Split days into weeks (lists of 7)
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    context = {
        'students':  students,
        'subjects':  subjects,
        'upcoming_exams': upcoming_exams,
        'papers_To_Grade':  papers_To_Grade,
        'Teacher':  Teacherr,
        'weeks': weeks,
        'month_name': calendar.month_name[month],
        'year': year
    }
    return render(request, 'teachers/teacher_dashboard.html', context)

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name   = request.POST.get('first_name')
        last_name    = request.POST.get('last_name')
        teacher_id   = request.POST.get('teacher_id')
        subject      = request.POST.get('subject')
        mobile       = request.POST.get('mobile_number')
        dept_id      = request.POST.get('department')
        image        = request.FILES.get('teacher_image')
        department   = get_object_or_404(Department, id=dept_id)
        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            subject=subject,
            mobile_number=mobile,
            department=department,
            teacher_image=image,
        )
        messages.success(request, 'Teacher added successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/add_teacher.html', {'departments': departments})

def edit_teacher(request, id):
    teacher     = get_object_or_404(Teacher, id=id)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name   = request.POST.get('first_name')
        teacher.last_name    = request.POST.get('last_name')
        teacher.subject      = request.POST.get('subject')
        teacher.mobile_number = request.POST.get('mobile_number')
        dept_id              = request.POST.get('department')
        teacher.department   = get_object_or_404(Department, id=dept_id)
        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES.get('teacher_image')
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/edit_teacher.html',
                  {'teacher': teacher, 'departments': departments})

def view_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    return render(request, 'teachers/teacher_details.html', {'teacher': teacher})

def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully!')
    return redirect('teacher_list')
def exams_teacher(request):
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    subjects = Subject.objects.filter(Teacher=teacher)

    upcoming_exams = Exam.objects.filter(
        subject__in=subjects,
        exam_date__gt=timezone.now()
    )

    past_exams = Exam.objects.filter(
        subject__in=subjects,
        exam_date__lte=timezone.now()
    )

    return render(request, 'teachers/exams_teacher.html', {
        'upcoming_exams': upcoming_exams,
        'past_exams': past_exams,
        'Teacher':  teacher,
    })
def courses_teacher(request):
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    subjects = Subject.objects.filter(Teacher=teacher)

    return render(request, 'teachers/courses_teacher.html', {
        'subjects': subjects,
        'Teacher':  teacher,
    })
def holidays_teacher(request):
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    holidays= Holiday.objects.all()

    return render(request, 'teachers/holiday.html', {
        'holidays': holidays,
        'Teacher':  teacher,
    })

def add_exam(request):
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    holidays= Holiday.objects.all()

    return render(request, 'teachers/courses_teacher.html', {
        'holidays': holidays,
        'Teacher':  teacher,
    })
def edit_exam(request):
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    holidays= Holiday.objects.all()

    return render(request, 'teachers/courses_teacher.html', {
        'holidays': holidays,
        'Teacher':  teacher,
    })
def delete_exam(request,id):
  Exam.objects.filter(id=id).delete()

  return render('teachers/exams_teacher.html')
