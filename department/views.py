from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', 
                  {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        name        = request.POST.get('name')
        description = request.POST.get('description')
        Department.objects.create(name=name, description=description)
        messages.success(request, 'Department added successfully!')
        return redirect('department_list')
    return render(request, 'departments/add_department.html')

def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        department.name        = request.POST.get('name')
        department.description = request.POST.get('description')
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('department_list')
    return render(request, 'departments/edit_department.html', 
                  {'department': department})

def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    messages.success(request, 'Department deleted successfully!')
    return redirect('department_list')