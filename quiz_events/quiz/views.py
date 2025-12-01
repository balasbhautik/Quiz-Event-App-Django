from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.db.models import Count

from quiz.models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event

# Create your views here.

def home(request):
    """
    Display the home page with the user's quiz submissions.
    Redirects to login if the user is not authenticated.
    """

    if request.user.is_authenticated:
        submissions = UserSubmission.objects.filter(user=request.user).select_related('user').order_by('-submitted_at')
        return render(request,'quiz/home.html', {'submissions': submissions, 'total_submissions': submissions.count()})
    else:
        return redirect('login')


def quiz_list(request):
    """
    Show all quizzes that contain at least one question.
    Redirects to login if the user is not authenticated.
    """

    if request.user.is_authenticated:
        quizzes = Quiz.objects.annotate(
            question_count=Count("questions")
        ).filter(question_count__gt=0).order_by('-created_at')
        return render(request, 'quiz/quiz_list.html',{'quizzes': quizzes})
    else:
        return redirect('login')


def start_quiz(request, quiz_id):
    """
    Display the quiz and handle answer submission.
    Creates a UserSubmission, evaluates answers, calculates score 
    and redirects to quiz result.
    """

    if request.user.is_authenticated:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        if request.method == "POST":
            submission = UserSubmission.objects.create(
                quiz = quiz,
                user = request.user,
                score = 0,
            )
            score = 0
            for q in questions:
                field_name = f"question_{q.id}"
                user_answer_value = request.POST.get(field_name)
                
                if not user_answer_value:
                    UserAnswer.objects.create(
                        submission = submission,
                        question = q,
                        answer = "",
                        is_correct = False
                    )
                    continue
                if q.question_type == "MCQ":
                    selected_answer = Answer.objects.get(id=user_answer_value)
                    is_correct = selected_answer.is_correct
                    
                    UserAnswer.objects.create(
                        submission=submission,
                        question = q,
                        answer = selected_answer,
                        is_correct = is_correct
                    )
                    if is_correct:
                        score = score + 1

                elif q.question_type == 'BOOL':
                    correct = q.answers.filter(is_correct=True).first()
                    is_correct = (correct.text.lower() == user_answer_value.lower())
                    UserAnswer.objects.create(
                        submission = submission,
                        question = q,
                        answer = user_answer_value,
                        is_correct = is_correct
                    )
                    if is_correct:
                        score = score + 1

                elif q.question_type == "TEXT":
                    correct = q.answers.filter(is_correct=True).first()

                    is_correct = (
                        correct and 
                        correct.text.strip().lower() == user_answer_value.strip().lower()
                    )

                    UserAnswer.objects.create(
                        submission=submission,
                        question=q,
                        answer=user_answer_value,
                        is_correct=is_correct
                    )

                    if is_correct:
                        score += 1        

            submission.score = score
            submission.save()

            return redirect('quiz_result', submission.id)                


        return render(request, 'quiz/start_quiz.html', {
            'quiz': quiz,
            'questions': questions
        })
    else:
        return redirect('login')


def quiz_result(request, submission_id):
    """
    Display the quiz result and user's submitted answers.
    """
    
    if request.user.is_authenticated:
        submission = get_object_or_404(UserSubmission, id=submission_id)
        user_answers = submission.answers.select_related('question')

        return render(request, 'quiz/quiz_result.html', {
            'submission': submission,
            'user_answers': user_answers
        })
    else:
        return redirect('login')


class EventListView(ListView):
    """
    This class is used to listing updating events.
    """
    
    queryset = Event.objects.all()
    template_name = 'quiz/event_list.html'
    context_object_name = 'events'


    def get_queryset(self):
        today = timezone.localdate()
        return Event.objects.filter(event_date__gte=today)
    

class EventDetailView(DetailView):
    """
    This class is used to Event Detail View.
    """
    queryset = Event.objects.all()
    template_name = 'quiz/event_details.html'
    context_object_name = 'event'
    pk_url_kwarg = 'id'
    query_pk_and_slug = 'id'

