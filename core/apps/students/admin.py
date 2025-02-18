from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student, StudentHomework, StudentHomeworkFile, StudentTestAttempt


class StudentHomeworkFileInline(admin.TabularInline):
    model = StudentHomeworkFile
    extra = 1


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')


@admin.register(StudentHomework)
class StudentHomeworkAdmin(admin.ModelAdmin):
    list_display = ('student', 'section_homework', 'is_late', 'number_of_files', 'created_at')
    list_filter = ('created_at', 'student')
    search_fields = ('student__email', 'section_homework__title')
    raw_id_fields = ('student', 'section_homework')
    inlines = [StudentHomeworkFileInline]


@admin.register(StudentTestAttempt)
class StudentTestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'is_passing', 'letter_grade', 'created_at')
    list_filter = ('created_at', 'student', 'test')
    search_fields = ('student__email', 'test__title')
    raw_id_fields = ('student', 'test')
    readonly_fields = ('score', 'is_passing', 'letter_grade', 'attempts_left')