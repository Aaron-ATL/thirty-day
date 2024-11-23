from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main_app.models import Profile, QuizQuestion, Lesson


@login_required
def start_quiz(request):
    profile = Profile.objects.get(user=request.user)
    lesson = Lesson.objects.get(pk=request.GET.get("pk"))
    questions_already_done = profile.progress_info.get("questions_answered_correctly")
    all_lesson_questions = lesson.questions.all()
    questions_not_done = all_lesson_questions.exclude(pk__in=questions_already_done)
    profile.progress_info["current_quiz"] = list(set(questions_not_done.values_list('pk', flat=True)))
    profile.save()
    
    question_data = questions_not_done.values().first()

    return JsonResponse({"question_data": question_data})
        
@login_required
def process_answer(request):
    profile = Profile.objects.get(user=request.user)
    index = int(request.GET.get("index"))
    current_quiz = profile.progress_info.get("current_quiz")
    if index == len(current_quiz):
        return JsonResponse({})
    index += 1
    next_pk = current_quiz[index]
    question_data = QuizQuestion.objects.filter(pk=next_pk).values().first()
    return JsonResponse({"question_data": question_data})
    
    # questions_already_done = set(profile.progress_info.get('questions_answered_correctly', []))
    # questions_already_done.add(question_pk)
    # profile.progress_info["questions_answered_correctly"] = list(questions_already_done)
    
    # profile.save()

    # return JsonResponse({"status": "success"})

@login_required
def reset_quiz(request):
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