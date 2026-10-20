from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Course, CourseMember, CourseContent, Comment

def core(request):
    return render(request, 'core.html')

def users(request):
    myusers = User.objects.all()
    context = {'myusers': myusers}
    return render(request, 'all_users.html', context)

def courses(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'all_courses.html', context)

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    ordering = ['-created_at']

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'


@login_required
def join_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    member, created = CourseMember.objects.get_or_create(
        course_id=course,
        user_id=request.user,
        defaults={'roles': 'std'}
    )
    if created:
        messages.success(request, f"Kamu berhasil bergabung di {course.name}")
    else:
        messages.info(request, f"Kamu sudah terdaftar di {course.name}")
    return redirect('course_detail', pk=pk)


@login_required
def course_content_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    contents = CourseContent.objects.filter(course_id=course)
    return render(request, 'course_content_list.html', {
        'course': course,
        'contents': contents
    })


@login_required
def course_content_detail(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    comments = Comment.objects.filter(content_id=content)
    return render(request, 'course_content_detail.html', {
        'content': content,
        'comments': comments
    })


@login_required
def add_comment(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    member = CourseMember.objects.filter(course_id=content.course_id, user_id=request.user).first()

    if not member:
        messages.error(request, "Kamu belum tergabung di mata kuliah ini.")
        return redirect('course_detail', pk=content.course_id.id)

    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(content_id=content, member_id=member, comment=text)
            messages.success(request, "Komentar berhasil ditambahkan.")
        return redirect('course_content_detail', content_id=content.id)

    return render(request, 'add_comment.html', {'content': content})


@login_required
def my_courses(request):
    memberships = CourseMember.objects.filter(user_id=request.user)
    return render(request, 'my_courses.html', {'memberships': memberships})
