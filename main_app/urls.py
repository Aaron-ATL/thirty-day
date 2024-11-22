from django.urls import path, include
from .views.user_views import (
    LessonListView,
    complete_lesson,
    make_member,
    webhook,
)
from .views.quiz_views import (
    GetQuizQuestionsView
)

urlpatterns = [
    path('', LessonListView.as_view(), name='index'),
    path('ajax/complete-lesson/', complete_lesson, name='complete-lesson'),
    path('ajax/start-quiz/', GetQuizQuestionsView.as_view(), name='start-quiz'),
    path('ajax/make-member/', make_member, name='make-member'),
    path('webhook/', webhook),
]