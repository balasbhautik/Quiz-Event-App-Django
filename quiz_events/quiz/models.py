from django.db import models
from user_accounts.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quizzes"           
        verbose_name_plural = "Quizzes"  

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE = (
        ('MCQ','Multiple Choice'),
        ('TEXT', 'Text Answer'),
        ('BOOL', 'True/False')
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE, default='TEXT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:20]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}"


class UserSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions_qns')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions_ans')
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    

class UserAnswer(models.Model):
    submission = models.ForeignKey(UserSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.user.username} - {self.question.text[:30]}"


class Event(models.Model):
    event_title = models.CharField(max_length=100)
    event_desc = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.event_title} - {self.event_date} - {self.location}"