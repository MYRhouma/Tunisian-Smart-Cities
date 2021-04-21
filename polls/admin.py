from django.contrib import admin

from .models import Question, Choice, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}),]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
class AnswerAdmin(admin.ModelAdmin):
    list_filter = ['question',]
admin.site.register(Answer,AnswerAdmin)