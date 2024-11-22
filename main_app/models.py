from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_activation_email
# Create your models here.

class Lesson(models.Model):
    number = models.IntegerField(default=1)
    title = models.CharField(max_length=200, default="Lesson X")
    description = models.TextField(default="Enter description")
    vimeo_id = models.CharField(max_length=50, default="000000000")
    length = models.IntegerField(default=5)  # rounded minutes
    thumbnail_id = models.IntegerField(default=100)
    lesson_file = models.CharField(max_length=60, default="lesson_file")

    def __str__(self):
        return f"{self.number}. {self.title}"

    class Meta:
        ordering = ["number"]

class Quiz(models.Model):
    lesson = models.OneToOneField(to=Lesson, on_delete=models.CASCADE, primary_key=True)
    question = models.CharField(max_length=255, default="Question")
    
    def __str__(self):
        return f"{self.lesson.title}"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    correct_answer = models.IntegerField()
    audio_file = models.CharField(max_length=30)
    
    def __str__(self):
        return f"Lesson {self.quiz.lesson.number}: {self.text}"
        
    class Meta:
        ordering = ["answer_id"]
       
class Profile(models.Model):
    def default_progress_info():
        return {
            "completed_lessons":[]
        }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress_info = models.JSONField(default=default_progress_info)
    community_member = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_invite(sender, instance, created, **kwargs):
    if created:
        send_activation_email(instance)