from django.contrib import admin
from quiz.models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event

# Register your models here.

@admin.register(Quiz)
class QuizModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_at','updated_at']
    search_fields = ['title', 'created_at']

@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz','question_type','created_at']
    search_fields = ['question_type']


@admin.register(Answer)
class AnswerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']


@admin.register(UserSubmission)
class UserSubmissionModelAdmin(admin.ModelAdmin):
    list_display = ['id','quiz','user', 'submitted_at']
    search_fields = ['user','submitted_at']


@admin.register(UserAnswer)
class UserAnswerModelAdmin(admin.ModelAdmin):
    list_display = ['submission','question','is_correct']
    

@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ['id','event_title', 'event_date', 'location']
    search_fields = ['event_title', 'location']
        


