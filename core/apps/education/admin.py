from django.contrib import admin

from .models import Institution, Course, Section, SectionFile, SectionHomework, SectionTest


class SectionFileInline(admin.TabularInline):
    model = SectionFile
    extra = 1


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'owner', 'number_of_courses', 'number_of_admins')
    list_filter = ('type',)
    search_fields = ('title', 'owner__email')
    filter_horizontal = ('admins',)
    raw_id_fields = ('owner',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'number_of_sections', 'number_of_teachers', 'number_of_students')
    list_filter = ('institution',)
    search_fields = ('title', 'institution__title')
    filter_horizontal = ('teachers', 'students')
    raw_id_fields = ('institution',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'type', 'number_of_files')
    list_filter = ('type', 'course')
    search_fields = ('title', 'course__title')
    raw_id_fields = ('course',)
    inlines = [SectionFileInline]


@admin.register(SectionHomework)
class SectionHomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'deadline', 'all_students_submitted')
    list_filter = ('deadline',)
    search_fields = ('title', 'section__title')
    raw_id_fields = ('section',)


@admin.register(SectionTest)
class SectionTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'max_score', 'passing_score', 'start_date', 'end_date', 'is_open')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'section__title')
    raw_id_fields = ('section',)