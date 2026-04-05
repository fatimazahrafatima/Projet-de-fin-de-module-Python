from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('course/add', views.add_subject, name='add_subject'),
    path('course/edit/<int:id>/', views.edit_subject, name='edit_subject'),
    path('ourse/delete/<int:id>/', views.delete_subject, name='delete_subject'),

]