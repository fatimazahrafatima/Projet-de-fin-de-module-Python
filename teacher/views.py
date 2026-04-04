from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher
from department.models import Department

def dashboard(request):
    teachers    = Teacher.objects.all()
    departments = Department.objects.prefetch_related('teacher_set').all()
    context = {
        'teachers':         teachers,
        'departments':      departments,
        'total_teachers':   teachers.count(),
        'total_departments': departments.count(),
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