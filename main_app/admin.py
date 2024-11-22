from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    Lesson, Profile, Quiz, QuizQuestion,
)

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.site_header = 'Thirty Day Bassist'
admin.site.index_title = 'Database access' 
admin.site.site_title = 'Admin'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Lesson)
admin.site.register(Profile)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)