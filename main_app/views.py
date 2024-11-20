from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from json import loads as json_loads
from .utils import webhook_is_verified, has_purchased_course, send_activation_email, create_user
from .models import Lesson, Profile, User
from .forms import CustomAuthenticationForm

# Create your views here.

class LessonListView(ListView):
    template_name = "main_app/course_list_view.html"
    model = Lesson
    context_object_name = "lessons"
    ordering = ['number']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['completed_lessons'] = profile.progress_info.get('completed_lessons')
        return context

def complete_lesson(request):
    profile = Profile.objects.get(user=request.user)
    completed_lessons = set(profile.progress_info["completed_lessons"])
    completed_lessons.add(int(request.GET.get("pk")))
    profile.progress_info["completed_lessons"] = list(completed_lessons)
    profile.save()
    return JsonResponse({})
    
def make_member(request):
    profile = Profile.objects.get(user=request.user)
    profile.community_member = True
    profile.save()
    return JsonResponse({})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    
@csrf_exempt
def webhook(request):
    if webhook_is_verified(request.body, request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256')):
        if has_purchased_course(str(request.body)):
            customer_email = json_loads(request.body)["email"].lower()
            if User.objects.filter(username=customer_email).exists():
                user = User.objects.get(username=customer_email)
                send_activation_email(user)
            else:
                create_user(customer_email)
    return HttpResponse(status=200)