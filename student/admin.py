from django.contrib import admin
from .models import Exam, ExamResult, Parent, Subject, Student,Holiday


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'exam_type', 'exam_date', 'duration', 'total_marks')
    list_filter = ('subject', 'exam_type', 'exam_date')
    search_fields = ('title', 'subject__name')
    ordering = ('-exam_date',)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'status', 'grade')
    list_filter = ('status', 'exam__subject', 'exam__exam_type')
    search_fields = ('student__name', 'exam__title')
    ordering = ('-exam__exam_date',)
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
 list_display = ('father_name', 'mother_name',
 'father_mobile', 'mother_mobile')
 search_fields = ('father_name', 'mother_name',
 'father_mobile', 'mother_mobile')
 list_filter = ('father_name', 'mother_name')
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
 def get_class(self, obj):
        return ", ".join([subject.name for subject in obj.student_class.all()])
 list_display = ('first_name', 'last_name', 'student_id',
 'gender', 'date_of_birth', 'get_class',
 'joining_date', 'mobile_number',
 'admission_number', 'section')
 search_fields = ('first_name', 'last_name', 'student_id',
 'get_class', 'admission_number')
 list_filter = ('gender', 'section')
 readonly_fields = ('student_image',)
@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end')
    search_fields = ('name',)