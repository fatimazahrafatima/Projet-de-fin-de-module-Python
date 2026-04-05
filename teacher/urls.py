from django.urls import path
from . import views
from student import views as student_views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('edit/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('dashboard/', views.dashboard, name='teacher_dashboard'),
    path('exams/', views.exams_teacher, name='exams_teacher'),
    path('exam/add', views.add_exam, name='add_exam'),
    path('exam/edit/<int:id>/', views.edit_exam, name='edit_exam'),
    path('exam/delete/<int:id>/', views.delete_exam, name='delete_exam'),
    path('courses/', views.courses_teacher, name='courses_teacher'),
    path('holidays/', views.holidays_teacher, name='holidays_teacher'),
    path('exam_resuts/add/<int:id>/', views.add_exam_results, name='add_exam_resuts'),

]
