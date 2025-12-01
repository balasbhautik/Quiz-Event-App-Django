from django.urls import path
from api.views import *

urlpatterns = [
    path('user/signup/', UserSignupAPIView.as_view(), name='user-signup'),
    path('user/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('user/profile-update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('user/user-change-password/', UserChangePasswordAPIView.as_view(), name='user-change-password'),
    path('user/user-detail/', UserDetailAPIView.as_view(), name='user-detail'),
    path('quiz/quiz-list/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quiz/start/<int:quiz_id>/', StartQuizAPI.as_view(), name='start-quiz-api'),
    path('quiz/user-submission-list/', UserSubmissionListView.as_view(), name='user-submission-list'),
    path('quiz/result/<int:submission_id>/', UserResultRetrieveView.as_view(), name='quiz-result'),
    path('quiz/event-list/', EventListAPIView.as_view(), name='event-list'),
    path('quiz/event-retrieve/<int:id>/', EventRetrieveAPIView.as_view(), name='event-retrieve')    

]
