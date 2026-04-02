from django.shortcuts import render, redirect
from .models import Teacher

# 📋 Liste des enseignants
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher-list.html', {'teachers': teachers})

# ➕ Ajouter un enseignant
def add_teacher(request):
    if request.method == 'POST':
        Teacher.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            teacher_id=request.POST.get('teacher_id'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            address=request.POST.get('address'),
            joining_date=request.POST.get('joining_date'),
        )
        return redirect('teacher_list')

    return render(request, 'teachers/add-teacher.html')

# ✏️ Modifier
def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)

    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.email = request.POST.get('email')
        teacher.save()
        return redirect('teacher_list')

    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher})

# ❌ Supprimer
def delete_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    teacher.delete()
    return redirect('teacher_list')