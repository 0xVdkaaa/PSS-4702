from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Nah ini yang diganti, abis logout langsung dilempar ke 'home'
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('api/course-stat/', views.course_stat_api, name='course_stat_api'),
]