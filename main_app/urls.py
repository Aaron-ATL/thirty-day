from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    LessonListView,
    complete_lesson,
    make_member,
    webhook,
)

urlpatterns = [
    path('', login_required(LessonListView.as_view()), name='index'),
    path('ajax/complete-lesson/', complete_lesson, name='complete-lesson'),
    path('ajax/make-member/', make_member, name='make-member'),
    path('webhook/', webhook),
]