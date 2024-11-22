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
        
class AnswerQuestionCorrectlyView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        question_pk = request.GET.get("pk")

        question = QuizQuestion.objects.get(pk=question_pk)
        
        questions_already_done = set(profile.progress_info.get('questions_answered_correctly', []))
        questions_already_done.add(question_pk)
        profile.progress_info["questions_answered_correctly"] = list(questions_already_done)
        
        profile.save()

        return JsonResponse({"status": "success"})

class ResetQuizView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        lesson_pk = int(request.GET.get("pk"))
        lesson = Lesson.objects.get(lesson_pk)

        all_lesson_questions = lesson.questions.all()
        question_pks_to_remove = set(all_lesson_questions.values_list('pk', flat=True))

        questions_already_done = set(profile.progress_info.get('questions_answered_correctly', []))
        updated_questions = questions_already_done - question_pks_to_remove
        profile.progress_info["questions_answered_correctly"] = list(updated_questions)

        profile.save()

        return JsonResponse({"status": "success"})