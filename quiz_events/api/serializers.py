from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from user_accounts.models import User
from quiz.models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


class UserSignupSerializer(serializers.ModelSerializer):
    """
    This serializer class is used for user signup.
    """
    confirm_password = serializers.CharField(max_length=100,style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']



    def validate(self, attrs):
        attrs =  super().validate(attrs)
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('The confirmation password does not match the password. Please try again.')
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class UserLoginserializer(serializers.ModelSerializer):
    """
    Serializer class used for user login authentication.
    """
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileUpdateSerializer(UserSignupSerializer):
    """
    Serializer class used to update the current user's profile.
    Username and email are read-only.
    """
    class Meta(UserSignupSerializer.Meta):
        read_only_fields = ['username', 'email']
        fields = ['first_name', 'last_name', 'username','email', 'profile_pic']
        

class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer class used to change the password of the current user.
    """
    current_password = serializers.CharField(max_length=100, style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=100, style={'input_type':'password'}, write_only=True)


    def validate(self, attrs):
        attrs =  super().validate(attrs)
        user = self.context.get('user')
        if not check_password(attrs.get('current_password'), user.password):
            raise serializers.ValidationError('Current password is incorrect.')
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('The confirmation password does not match the password. Please try again.')
        return attrs
    
    def save(self, **kwargs):
        password = self.validated_data.get('password', None)
        user = self.context.get('user', None)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(UserSignupSerializer):
    """
    Serializer class to retrieve detailed information of a user.
    """
    profile_pic = serializers.SerializerMethodField()
    class Meta(UserSignupSerializer.Meta):
        fields = ['first_name', 'last_name','username','email', 'profile_pic']
        read_only_fields = ['first_name', 'last_name','username','email','profile_pic']
    
    def get_profile_pic(self, obj):
        request = self.context.get('request')
        if obj.profile_pic:
            return request.build_absolute_uri(obj.profile_pic.url)
        return None
        

class QuizListSerializer(serializers.ModelSerializer):
    """
    Serializer class to list quiz details.
    """
    class Meta:
        model = Quiz
        fields = ['id', 'title','description','created_at','updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent quiz answers.
    """
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent quiz questions with their answers.
    """
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'answers']


class QuizDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent detailed information of a quiz, including its questions and answers.
    """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']


class SubmitQuizSerializer(serializers.Serializer):
    """
    Serializer class for submitting quiz answers.
    """
    answers = serializers.DictField(
        child=serializers.CharField(),
        help_text="Dictionary: question_id → answer"
    )


class UserSubmissionListSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent a user's quiz submission details.
    """
    quiz = QuizListSerializer()
    user = UserDetailSerializer()
    total_submission = serializers.SerializerMethodField()
    class Meta:
        model = UserSubmission
        fields = ['id','quiz', 'user', 'score', 'total_submission','submitted_at']

    def get_total_submission(self, obj):
        return UserSubmission.objects.filter(user=obj.user).count()    


class UserAnswerResultSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent a user's answer along with the correct answer.
    """
    question_text = serializers.CharField(source="question.text")
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = UserAnswer
        fields = ['question_text', 'answer', 'is_correct', 'correct_answer']


    def get_correct_answer(self, obj):
        correct = obj.question.answers.filter(is_correct=True).first()
        return correct.text if correct else None


class UserSubmissionResultSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent a user's quiz submission result in detail.
    """
    quiz_title = serializers.CharField(source="quiz.title")
    answers = UserAnswerResultSerializer(many=True)

    class Meta:
        model = UserSubmission
        fields = [
            'id',
            'quiz_title',
            'score',
            'submitted_at',
            'answers',
        ]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer class to represent event details.
    """
    class Meta:
        model = Event
        fields = ['id','event_title','event_desc','event_date','location']
        