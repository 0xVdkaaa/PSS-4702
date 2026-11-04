from django.urls import path
from coreapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course-stat/', views.courseStat, name='courseStat'),
    path('user-stat/', views.userStat, name='userStat'),
    path('courses/', views.course_list, name='courses'),
    path('mahasiswa/', views.mahasiswa_list, name='mahasiswa_list'),
]