from django.contrib import admin
from django.urls import path, include
from coreapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('course-stat/', views.courseStat, name='courseStat'),
    path('user-stat/', views.userStat, name='userStat'),
    path('courses/', views.course_list, name='courses'),
]