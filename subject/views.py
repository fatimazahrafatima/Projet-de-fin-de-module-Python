from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Subject
from teacher.models import Teacher
from department.models import Department
from django.contrib import messages

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject_list.html',
                  {'subjects': subjects})


def add_subject(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description")
        department_id = request.POST.get("department")
        teacher_id = request.POST.get("teacher")

        department = Department.objects.get(id=department_id)

        teacher = None
        if teacher_id:
            teacher = Teacher.objects.get(id=teacher_id)

        Subject.objects.create(
            name=name,
            code=code,
            description=description,
            department=department,
            Teacher=teacher
        )
        messages.success(request, 'subject added !')
        return redirect("courses_teacher")  
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'subjects/add_subject.html', {
        "departments": departments,
        "teachers": teachers
    })

def edit_subject(request, id):
    subject     = get_object_or_404(Subject, id=id)
    departments = Department.objects.all()
    if request.method == 'POST':
        subject.name        = request.POST.get('name')
        subject.code        = request.POST.get('code')
        subject.description = request.POST.get('description')
        dept_id             = request.POST.get('department')
        subject.department  = get_object_or_404(Department, id=dept_id)
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('courses_teacher')
    return render(request, 'subjects/edit_subject.html',
                  {'subject': subject, 'departments': departments})

def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully!')
    return redirect('courses_teacher')