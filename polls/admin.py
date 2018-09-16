from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    """Sets up the admin for choices to be inline with the Question the
    choice belongs to, and shows 3 extra slots for choices.
    """
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """
    This sets up the admin view of the question model with fieldsets to
    group differet aspects of the question.
    """
    fieldsets = [
        (None,          {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['question_text']

# Register models
admin.site.register(Question, QuestionAdmin)
