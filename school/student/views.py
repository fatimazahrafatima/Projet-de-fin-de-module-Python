from django.shortcuts import render, redirect
from .models import Student, Parent

def student_list(request):
    return render(request, 'students/students.html')

def add_student(request):
    return render(request, 'students/add-student.html')