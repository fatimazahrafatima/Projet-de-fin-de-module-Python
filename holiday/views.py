from django.shortcuts import render, redirect
from .models import Holiday
from teacher.models import Teacher
from django.contrib import messages
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holiday-list.html', {'holidays': holidays})

def add_holiday(request):

    if request.method == "POST":
        name = request.POST.get("name")
        date_start = request.POST.get("date_start")
        date_end = request.POST.get("date_end")
        description = request.POST.get("description")

        Holiday.objects.create(
            name=name,
            date_start=date_start,
            date_end=date_end,
            description=description
        )
        messages.success(request, 'holiday added!')
        return redirect('add_holiday')  
    user=request.user
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'holidays/add_holiday.html')

def delete_holiday(request, pk):
    Holiday.objects.filter(pk=pk).delete()
    return redirect('holidays_teacher')