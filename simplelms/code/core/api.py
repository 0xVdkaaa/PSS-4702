from typing import List
from ninja import NinjaAPI, Schema, Field
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Course, CourseMember
from ninja_simple_jwt.auth.views.api import web_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth

api = NinjaAPI(title="Simple LMS API", version="1.0.0",
               description="REST API untuk Simple LMS (Django Ninja)")

api.add_router("/auth", web_auth_router)


class CourseIn(Schema):
    name: str
    description: str = '-'
    price: int = 10000
    teacher_id: int


class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int
    teacher_id: int


class MemberOut(Schema):
    id: int
    course_id: int
    user_id: int
    roles: str


@api.get("/courses", response=List[CourseOut])
def list_courses(request):
    return Course.objects.all()


# ---------- Pertemuan 10: Throttling, Pagination, Filtering, Sorting ----------
from ninja.pagination import paginate, PageNumberPagination
from ninja.throttling import AnonRateThrottle
from ninja import FilterSchema, Query
from typing import Optional


class CourseFilter(FilterSchema):
    search: Optional[str] = Field(None, q='name__icontains')
    price: Optional[int] = Field(None, q='price')


@api.get("/courses/browse", response=List[CourseOut],
         throttle=AnonRateThrottle("10/m"))
@paginate(PageNumberPagination, page_size=5)
def browse_courses(request, filters: CourseFilter = Query(...),
                   sort: str = "id"):
    qs = Course.objects.all()
    qs = filters.filter(qs)
    if sort in ("price", "-price", "name", "-name"):
        qs = qs.order_by(sort)
    return qs


@api.get("/courses/{course_id}", response=CourseOut)
def get_course(request, course_id: int):
    return get_object_or_404(Course, id=course_id)


@api.post("/courses", response={201: CourseOut}, auth=HttpJwtAuth())
def create_course(request, payload: CourseIn):
    teacher = get_object_or_404(User, id=payload.teacher_id)
    course = Course.objects.create(
        name=payload.name, description=payload.description,
        price=payload.price, teacher=teacher)
    return 201, course


@api.put("/courses/{course_id}", response=CourseOut, auth=HttpJwtAuth())
def update_course(request, course_id: int, payload: CourseIn):
    course = get_object_or_404(Course, id=course_id)
    teacher = get_object_or_404(User, id=payload.teacher_id)
    course.name = payload.name
    course.description = payload.description
    course.price = payload.price
    course.teacher = teacher
    course.save()
    return course


@api.delete("/courses/{course_id}", response={204: None}, auth=HttpJwtAuth())
def delete_course(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return 204, None


@api.get("/members", response=List[MemberOut])
def list_members(request):
    return CourseMember.objects.all()


class MeOut(Schema):
    username: str
    email: str


@api.get("/users/me", response=MeOut, auth=HttpJwtAuth())
def me(request):
    # user hasil decode JWT tersedia di request.user
    return {"username": request.user.username,
            "email": request.user.email}
