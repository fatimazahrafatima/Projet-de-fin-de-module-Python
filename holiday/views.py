from django.shortcuts import render, redirect
from .models import Holiday

def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holiday-list.html', {'holidays': holidays})

def add_holiday(request):
    if request.method == 'POST':
        Holiday.objects.create(
            name=request.POST.get('name'),
            date_start=request.POST.get('date_start'),
            date_end=request.POST.get('date_end'),
            description=request.POST.get('description'),
        )
        return redirect('holiday_list')
    return render(request, 'holidays/add-holiday.html')

def delete_holiday(request, pk):
    Holiday.objects.filter(pk=pk).delete()
    return redirect('holiday_list')