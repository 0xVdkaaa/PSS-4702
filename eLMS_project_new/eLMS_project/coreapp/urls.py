from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('api/course-stat/', views.course_stat_api, name='course_stat_api'),
    
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('course/<int:id>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Rute baru buat form upload materi dosen
    path('course/<int:id>/add-materi/', views.add_materi, name='add_materi'),
]