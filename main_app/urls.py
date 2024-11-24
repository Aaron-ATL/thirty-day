from django.urls import path, include
from .views.user_views import (
    LessonListView,
    complete_lesson,
    make_member,
    webhook,
)
from .views.quiz_views import (
    reset_quiz,
    start_quiz,
    process_answer
)

urlpatterns = [
    path('', LessonListView.as_view(), name='index'),
    path('quiz/start/', start_quiz, name='start-quiz'),
    path('quiz/answer/', process_answer, name='quiz-answer'),
    path('quiz/reset/', reset_quiz, name='quiz-reset'),
    path('ajax/complete-lesson/', complete_lesson, name='complete-lesson'),
    path('ajax/make-member/', make_member, name='make-member'),
    path('webhook/', webhook),
]