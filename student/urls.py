from django.urls import path
from . import views

urlpatterns = [
 path('', views.student_list, name='student_list'),
 path('dashboard/', views.student_dashboard, name='student_dashboard'),
 path('add/', views.add_student, name='add_student'),
 path('students/<str:student_id>/',
 views.view_student, name='view_student'),
 path('edit/<str:student_id>/',
 views.edit_student, name='edit_student'),
 path('delete/<str:student_id>/',
 views.delete_student, name='delete_student'),
 path('departments/', views.departmentsve, name='departmentsur'),
 path('Courses/', views.Courses_ve, name='Courses_ur'),
 path('Exams/', views.Exam_ve, name='Exam_ur'),
 path('grades/', views.grades_ve, name='grades_ur'),
]