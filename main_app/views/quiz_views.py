from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main_app.models import Profile, QuizQuestion, Lesson


@login_required
def start_quiz(request):
    profile = Profile.objects.get(user=request.user)
    lesson = Lesson.objects.get(pk=request.GET.get("lesson_pk"))
    questions_already_done = list(set(profile.progress_info.get("questions_answered_correctly")))
    all_lesson_questions = lesson.questions.all()
    questions_not_done = all_lesson_questions.exclude(pk__in=questions_already_done)
    stars_earned_on_this_lesson = len(all_lesson_questions) - len(questions_not_done)
    profile.progress_info["current_quiz"] = sorted(list(set(questions_not_done.values_list('pk', flat=True))))
    print(profile.progress_info["current_quiz"], questions_not_done.values_list('pk', flat=True))
    profile.save()
    
    if not questions_not_done:
        return JsonResponse({
            "message": "Quiz already completed.",
            "stars_earned_on_this_lesson": stars_earned_on_this_lesson
        })
    
    question_data = questions_not_done.values().first()

    return JsonResponse({"question_data": question_data,
                         "total_stars_available": len(all_lesson_questions),
                         "stars_earned_on_this_lesson": stars_earned_on_this_lesson})
        
@login_required
def process_answer(request):
    profile = Profile.objects.get(user=request.user)
    index = int(request.GET.get("index"))
    selected_answer = int(request.GET.get("active_answer_id"))

    # Retrieve the current quiz question IDs
    current_quiz_ids = sorted(list(profile.progress_info.get("current_quiz")))
    current_question_id = current_quiz_ids[index]
    current_question = QuizQuestion.objects.get(pk=current_question_id)
    
    # Check if the selected answer is correct
    answered_correctly = current_question.correct_answer == selected_answer

    # Update the list of correctly answered questions if the answer is correct
    if answered_correctly:
        questions_answered_correctly = set(profile.progress_info.get('questions_answered_correctly', []))
        questions_answered_correctly.add(current_question.pk)
        profile.progress_info["questions_answered_correctly"] = list(questions_answered_correctly)
        profile.save()

    # Move to the next question
    index += 1

    # Check if the quiz is completed
    if index == len(current_quiz_ids):
        all_correct = set(current_quiz_ids).issubset(profile.progress_info.get('questions_answered_correctly', []))
        return JsonResponse({
            "answered_correctly": answered_correctly,
            "all_correct": all_correct
        })
     
    return JsonResponse(
        {"question_data": prepare_question_data(current_quiz_ids[index]),
         "index": index,
         "answered_correctly": answered_correctly}
    )

@login_required
def reset_quiz(request):
    profile = Profile.objects.get(user=request.user)
    lesson_pk = int(request.GET.get("lesson_pk"))
    lesson = Lesson.objects.get(pk=lesson_pk)

    all_lesson_questions = lesson.questions.all()
    question_pks_to_remove = set(all_lesson_questions.values_list('pk', flat=True))

    questions_already_done = set(profile.progress_info.get('questions_answered_correctly', []))
    updated_questions = questions_already_done - question_pks_to_remove
    profile.progress_info["questions_answered_correctly"] = list(updated_questions)
    profile.progress_info["current_quiz"] = sorted(list(set(all_lesson_questions.values_list('pk', flat=True))))
    profile.save()
    
    question_data = all_lesson_questions.values().first()

    return JsonResponse({"question_data": question_data,
                         "stars_earned_on_this_lesson": 0,
                         "total_stars_available": len(all_lesson_questions)})

def prepare_question_data(pk):
    next_question = QuizQuestion.objects.get(pk=pk)
    return {
        "id": next_question.pk,
        "text": next_question.text,
        "answer_1": next_question.answer_1,
        "answer_2": next_question.answer_2,
        "answer_3": next_question.answer_3,
        "audio_file": next_question.audio_file,
    }

