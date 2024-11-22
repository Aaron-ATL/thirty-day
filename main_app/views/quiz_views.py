from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.models import Profile, QuizQuestion, Lesson

class GetQuizQuestionsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        lesson = Lesson.objects.get(pk=request.GET.get("pk"))
        questions_already_done = profile.progress_info.get("questions_answered_correctly")
        all_lesson_questions = lesson.questions.all()
        questions_not_done = all_lesson_questions.exclude(pk__in=questions_already_done)
        
        questions_data = list(questions_not_done.values(
            'id',
            'text',
            'answer_1',
            'answer_2',
            'answer_3',
            'correct_answer',
            'audio_file'
        ))
        print(questions_data)
        return JsonResponse({"questions": questions_data})