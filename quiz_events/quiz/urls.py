from django.urls import path
from quiz.views import *

urlpatterns = [
    path('', home, name='home'),
    path('all-quizees/', quiz_list, name='quiz_list'),
    path('start-quiz/<int:quiz_id>/', start_quiz, name='start_quiz'),
    path('quiz-result/<int:submission_id>/', quiz_result, name='quiz_result'),
    path('all-events/', EventListView.as_view(), name='all_events'),
    path('event-detail/<int:id>/', EventDetailView.as_view(), name='event_detail'),

]
