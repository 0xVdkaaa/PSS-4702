from django.urls import path
from . import views

urlpatterns = [
    path('', views.core, name='core'),
    path('users/', views.users, name='users'),
    path('courses/', views.courses, name='courses'),
    path('courses/list/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:pk>/join/', views.join_course, name='join_course'),
    path('course/<int:course_id>/contents/', views.course_content_list, name='course_content_list'),
    path('content/<int:content_id>/', views.course_content_detail, name='course_content_detail'),
    path('content/<int:content_id>/comment/', views.add_comment, name='add_comment'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
