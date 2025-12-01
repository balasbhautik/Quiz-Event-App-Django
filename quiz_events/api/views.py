from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view,OpenApiExample, inline_serializer, OpenApiResponse, OpenApiParameter

from user_accounts.models import User
from api.serializers import UserSignupSerializer, UserLoginserializer, UserProfileUpdateSerializer, UserChangePasswordSerializer, UserDetailSerializer,QuizListSerializer, QuizDetailSerializer, QuestionSerializer, SubmitQuizSerializer, UserSubmissionListSerializer, UserSubmissionResultSerializer, EventSerializer
from quiz.models import Quiz, Question, Answer,UserSubmission, UserAnswer, Event

from utils import custom_response, UserMessage, QuizMessage, UserSubmissionMessages, EventMessages

# Create your views here.

def get_token_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }


@extend_schema(
    summary="User Signup",
    description="Register a new user by providing name, email, password, etc.",
    request=UserSignupSerializer,

    responses={
        201: OpenApiResponse(
            inline_serializer(
                name="SignupSuccessResponse",
                fields={
                    "success": serializers.IntegerField(default=1),
                    "message": serializers.CharField(default="User signup successfully."),
                    "data": serializers.DictField(default=None, allow_null=True),
                }
            )
        ),
        400: OpenApiResponse(
            inline_serializer(
                name="SignupErrorResponse",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Validation error."),
                    "errors": serializers.JSONField()
                }
            )
        ),
    }
)
class UserSignupAPIView(APIView):
    """
    User registration (signup) API.

    Accepts user data and creates a new account if valid.

    **POST**:
    - Success (201): User registered successfully.
    - Failure (400): Validation errors returned.
    """
    def post(self, request, format=None):
        data = request.data
        serializer = UserSignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                request=request,
                message=UserMessage.USER_SIGNUP_SUCCESSFULLY,
                success=1,
                status_code = status.HTTP_201_CREATED
            )
        else:
            return custom_response(
                request=request,
                message=serializer.errors,
                success=0,
                status_code = status.HTTP_400_BAD_REQUEST
            )


class UserLoginAPIView(APIView):
    """
    This class is used for user authentication.
    """
    @extend_schema(
        summary="User Login API",
        description="Authenticate the user using email and password and returns JWT access & refresh tokens.",
        request=UserLoginserializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="LoginSuccessResponse",
                    fields={
                        "access": serializers.CharField(),
                        "refresh": serializers.CharField(),
                    }
                ),
                description="Login successful"
            ),
            400: OpenApiResponse(
                description="Invalid credentials",
                examples=[
                    OpenApiExample(
                        name="Invalid Login Example",
                        value={"message": "Login failed. Invalid email or password.", "success": 0}
                    )
                ]
            )
        },
        examples=[
            OpenApiExample(
                name="Login Example",
                request_only=True,
                value={
                    "email": "user@example.com",
                    "password": "password123"
                }
            )
        ]
    )
    def post(self, request, format=None):
        serializer = UserLoginserializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request=request, username=email, password=password)
            if user is not None:
                token = get_token_for_user(user)
                return custom_response(
                    request=request,
                    data=token,
                    message=UserMessage.USER_LOGIN_SUCCESSFULLY,
                    success=1,
                    status_code=status.HTTP_200_OK
                )
            else:
                return custom_response(
                    request=request,
                    message=UserMessage.USER_LOGIN_FAIL,
                    success=0,
                    status_code=status.HTTP_400_BAD_REQUEST
                )


@extend_schema(
    summary="Update User Profile",
    description="Allows an authenticated user to update their profile information.",
    request=UserProfileUpdateSerializer,
    responses={
        200: OpenApiResponse(
            inline_serializer(
                name="UserProfileUpdateSuccess",
                fields={
                    "success": serializers.IntegerField(default=1),
                    "message": serializers.CharField(default="User profile updated successfully."),
                    "data": serializers.DictField(default=None, allow_null=True),
                }
            )
        ),
        400: OpenApiResponse(
            inline_serializer(
                name="UserProfileUpdateError",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Validation error."),
                    "errors": serializers.JSONField()
                }
            )
        ),
        401: OpenApiResponse(
            inline_serializer(
                name="UserProfileUnauthorized",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Authentication credentials were not provided."),
                }
            )
        ),
    }
)      
class UserProfileUpdateAPIView(APIView):
    """
    This class is used to update the current user's profile.
    """        
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileUpdateSerializer(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                request=request,
                message=UserMessage.USER_PROFILE_UPDATE_SUCCESSFULLY,
                success=1,
                status_code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                request=request,
                message=serializer.errors,
                success=0,
                status_code=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    summary="Change User Password",
    description="Allows an authenticated user to change their current account password.",
    request=UserChangePasswordSerializer,
    responses={
        200: OpenApiResponse(
            inline_serializer(
                name="ChangePasswordSuccess",
                fields={
                    "success": serializers.IntegerField(default=1),
                    "message": serializers.CharField(default="Password changed successfully."),
                }
            )
        ),
        400: OpenApiResponse(
            inline_serializer(
                name="ChangePasswordError",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Validation error."),
                    "errors": serializers.JSONField()
                }
            )
        ),
        401: OpenApiResponse(
            inline_serializer(
                name="ChangePasswordUnauthorized",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Authentication credentials were not provided."),
                }
            )
        ),
    }
)
class UserChangePasswordAPIView(APIView):
    """
    This class is used to change the current user's password.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                request=request,
                message=UserMessage.USER_CHANGE_PASS_SUCCESSFULLY,
                success=1,
                status_code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                request=request,
                message=serializer.errors,
                success=0,
                status_code=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    summary="Get Current User Details",
    description="Returns the profile details of the currently authenticated user.",
    responses={
        200: OpenApiResponse(
            inline_serializer(
                name="UserDetailSuccess",
                fields={
                    "success": serializers.IntegerField(default=1),
                    "message": serializers.CharField(default="User details retrieved successfully."),
                    "data": UserDetailSerializer()
                }
            )
        ),
        401: OpenApiResponse(
            inline_serializer(
                name="UserDetailUnauthorized",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Authentication credentials were not provided."),
                }
            )
        ),
        500: OpenApiResponse(
            inline_serializer(
                name="UserDetailServerError",
                fields={
                    "success": serializers.IntegerField(default=0),
                    "message": serializers.CharField(default="Internal server error."),
                }
            )
        ),
    }
)
class UserDetailAPIView(APIView):
    """
    This class is used to retrieve details of the current logged-in user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            serializer = UserDetailSerializer(request.user, context={'request':request})
            return custom_response(
                request=request,
                data=serializer.data,
                message=UserMessage.USER_DETAIL_RETRIEVE_SUCCESSFULLY,
                success=1,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return custom_response(
                request=request,
                message=str(e),
                success=0,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuizListAPIView(ListAPIView):
    """
    This class is used to list all quizzes.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        return Quiz.objects.annotate(
            question_count=Count("questions")
        ).filter(question_count__gt=0).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return custom_response(
            request=request,
            data = response.data,
            message=QuizMessage.QUIZ_LIST_SUCCESSFULLY,
            success=1,
            status_code=status.HTTP_201_CREATED
        )


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve Quiz Details",
        description="Fetch a quiz with its questions and available answers.",
        parameters=[
            OpenApiParameter(name="quiz_id", description="Quiz ID", required=True, type=int)
        ],
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="QuizRetrieveSuccess",
                    fields={
                        "success": serializers.IntegerField(default=1),
                        "message": serializers.CharField(default="Quiz fetched successfully."),
                        "data": QuizDetailSerializer()
                    }
                )
            ),
            400: OpenApiResponse(
                inline_serializer(
                    name="QuizRetrieveError",
                    fields={
                        "success": serializers.IntegerField(default=0),
                        "message": serializers.CharField(default="Quiz not found.")
                    }
                )
            ),
            401: OpenApiResponse(
                inline_serializer(
                    name="QuizRetrieveUnauthorized",
                    fields={
                        "success": serializers.IntegerField(default=0),
                        "message": serializers.CharField(default="Authentication credentials were not provided.")
                    }
                )
            ),
        }
    ),
    # ------------------ POST SCHEMA ------------------
    post=extend_schema(
        summary="Submit Quiz Answers",
        description=(
            "Submit user answers for the quiz. Supports MCQ, TEXT, and BOOL questions.\n"
            "Request format:\n"
            "{\n"
            '   "answers": {\n'
            '       "1": "Mars",\n'
            '       "2": 5,\n'
            '       ...\n'
            '   }\n'
            "}"
        ),

        parameters=[
            OpenApiParameter(name="quiz_id", description="Quiz ID", required=True, type=int)
        ],

        request=inline_serializer(
            name="SubmitQuizRequest",
            fields={
                "answers": serializers.DictField(
                    child=serializers.CharField(),
                    help_text="Dictionary of question_id: user_answer"
                )
            }
        ),

        responses={
            200: OpenApiResponse(
                inline_serializer(
                    name="SubmitQuizSuccess",
                    fields={
                        "success": serializers.IntegerField(default=1),
                        "message": serializers.CharField(default="Quiz submitted successfully."),
                        "score": serializers.IntegerField(default=3),
                        "submission_id": serializers.IntegerField(default=10)
                    }
                )
            ),

            400: OpenApiResponse(
                inline_serializer(
                    name="SubmitQuizError",
                    fields={
                        "success": serializers.IntegerField(default=0),
                        "message": serializers.CharField(default="Invalid data provided.")
                    }
                )
            ),

            401: OpenApiResponse(
                inline_serializer(
                    name="SubmitQuizUnauthorized",
                    fields={
                        "success": serializers.IntegerField(default=0),
                        "message": serializers.CharField(default="Authentication required.")
                    }
                )
            ),
        }
    )
)
class StartQuizAPI(APIView):
    """
    Handles quiz retrieval and submission.
    GET:
        Returns quiz details with questions and answers.
    POST:
        Accepts user-submitted answers, evaluates them,
        creates a UserSubmission record, and returns the score.
    Requires:
        - JWT authentication
        - Authenticated user
    Payload (POST):
        {
            "answers": {
                "<question_id>": "<answer_value>"
            }
        }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return custom_response(
                request=request,
                message=QuizMessage.QUIZ_NOT_FOUND,
                success=0,
                status_code = status.HTTP_400_BAD_REQUEST
            )

        serializer = QuizDetailSerializer(quiz)
        return custom_response(
            request=request,
            data=serializer.data,
            message=QuizMessage.QUIZ_RETRIEVE_SUCCESSFULLY,
            success=1,
            status_code=status.HTTP_200_OK
        )
    

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return custom_response(
                request=request,
                message=QuizMessage.QUIZ_NOT_FOUND,
                success=0,
                status_code=status.HTTP_400_BAD_REQUEST
            ) 
        

        serializer = SubmitQuizSerializer(data=request.data)
        if not serializer.is_valid():         
            return custom_response(
                request=request,
                message=serializer.errors,
                success=0,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        answers = serializer.validated_data["answers"]
        questions = quiz.questions.all()

        submission = UserSubmission.objects.create(
            quiz=quiz,
            user=request.user,
            score=0
        )

        score = 0

        for q in questions:
            submitted_answer = answers.get(str(q.id), None)

            # If user did not send this question
            if not submitted_answer:
                UserAnswer.objects.create(
                    submission=submission,
                    question=q,
                    answer="",
                    is_correct=False
                )
                continue

            if q.question_type == "MCQ":
                try:
                    selected = Answer.objects.get(id=submitted_answer)
                except Answer.DoesNotExist:
                    selected = None

                is_correct = selected.is_correct if selected else False

                UserAnswer.objects.create(
                    submission=submission,
                    question=q,
                    answer=selected.text if selected else "",
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

            
            elif q.question_type == "BOOL":
                correct = q.answers.filter(is_correct=True).first()
                is_correct = (correct.text.lower() == submitted_answer.lower())

                UserAnswer.objects.create(
                    submission=submission,
                    question=q,
                    answer=submitted_answer,
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

            
            elif q.question_type == "TEXT":
                correct = q.answers.filter(is_correct=True).first()

                is_correct = (
                    correct and 
                    correct.text.strip().lower() == submitted_answer.strip().lower()
                )

                UserAnswer.objects.create(
                    submission=submission,
                    question=q,
                    answer=submitted_answer,
                    is_correct=is_correct
                )

                if is_correct:
                    score += 1

        submission.score = score
        submission.save()

        return custom_response(
            request=request,
            message=QuizMessage.QUIZ_SUBMITTED_SUCCESSFULLY,
            success=1,
            score=score,
            submission_id=submission.id,
            status_code=status.HTTP_200_OK
        )


class UserSubmissionListView(ListAPIView):
    """
    This class is used to retrieves a list of submissions for the current authenticated user.
    """
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return UserSubmission.objects.filter(user=self.request.user).select_related('user').order_by('-submitted_at')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return custom_response(
            request=request,
            data = response.data,
            message=UserSubmissionMessages.USER_SUBMISSION_RETRIEVE_SUCCESSFULLY,
            success=1,
            status_code=status.HTTP_200_OK
        )
    

@extend_schema(
    tags=['User - Quiz Result'],
    summary="Retrieve Quiz Result for a Submission",
    description=(
        "Fetches the quiz result of a specific submission (`submission_id`) "
        "that belongs to the currently authenticated user. "
        "Returns the quiz details, score, total questions, and each user's answer."
    ),
    responses={
        200: OpenApiResponse(
            response=UserSubmissionResultSerializer,
            description="Quiz result retrieved successfully"
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name="NotFoundResponse",
                fields={"detail": serializers.CharField()}
            ),
            description="Submission not found for this user"
        ),
        401: OpenApiResponse(
            response=inline_serializer(
                name="UnauthorizedResponse",
                fields={"detail": serializers.CharField()}
            ),
            description="Authentication credentials were not provided"
        ),
    }
)
class UserResultRetrieveView(APIView):
    """
    Fetch quiz result for a specific submission (submission_id),
    including all user answers and correctness.
    """
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, submission_id):
        submission = get_object_or_404(
            UserSubmission, 
            id=submission_id, 
            user=request.user   # only fetch current user's submission
        )

        serializer = UserSubmissionResultSerializer(submission)

        return custom_response(
            request=request,
            data=serializer.data,
            message=UserSubmissionMessages.USER_RESULT_RETRIEVE_SUCCESSFULLT,
            success=1,
            status_code=status.HTTP_200_OK
        )


class EventListAPIView(ListAPIView):
    """
    This is class is used to list all upcoming events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        today = timezone.localdate()
        return Event.objects.filter(event_date__gte=today)
    
    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs)
        return custom_response(
            request=request,
            data=response.data,
            message=EventMessages.EVENT_FETCHED_SUCCESSFULLY,
            success=1,
            status_code=status.HTTP_200_OK
        )


class EventRetrieveAPIView(RetrieveAPIView):
    """
    This class is used to retrieve specific event using event id.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_url_kwarg = 'id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        response =  super().retrieve(request, *args, **kwargs)
        return custom_response(
            request=request,
            data=response.data,
            message=EventMessages.EVENT_FETCHED_SUCCESSFULLY,
            success=1,
            status_code=status.HTTP_200_OK
        )