from django.urls import path, include
from .views.user_views import (
    LessonListView,
    complete_lesson,
    make_member,
    webhook,
)
from .views.quiz_views import (
    AnswerQuestionCorrectlyView,
    GetQuizQuestionsView,
    ResetQuizView
)

urlpatterns = [
    path('', LessonListView.as_view(), name='index'),
    path('quiz/get-questions/', GetQuizQuestionsView.as_view(), name='get_quiz_questions'),
    path('quiz/answer/', AnswerQuestionCorrectlyView.as_view(), name='answer_question_correctly'),
    path('quiz/reset/', ResetQuizView.as_view(), name='reset_quiz'),
    path('ajax/complete-lesson/', complete_lesson, name='complete-lesson'),
    path('ajax/make-member/', make_member, name='make-member'),
    path('webhook/', webhook),
]