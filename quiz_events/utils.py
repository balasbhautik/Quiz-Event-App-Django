import json
from rest_framework import status
from rest_framework.response import Response

from logentry.models import LogEntry

# This funcation is used to custom response for apis
def custom_response(request, data=None, success=0, message="", user=None, get_data=None, send_data=None, score=None,submission_id=None,status_code=status.HTTP_200_OK):
    if data is None:
        data = {}
    if get_data is None:
        get_data = request.GET.dict() 
    if send_data is None:
        send_data = data  

    if request.user.is_authenticated:
        user_obj = request.user
    else:
        user_obj = 'anonymous user'

    ip_address = request.META.get('REMOTE_ADDR')
    api_name = request.path
    api_type = request.method

    LogEntry.objects.create(
        user=str(user_obj),
        ip_address=ip_address,
        message=str(message),
        api_name=api_name,
        api_type=api_type,
        send_data=json.dumps(send_data),
        get_data=json.dumps(get_data),
        status=str(status_code)
    )
    
    if score is not None and submission_id is not None:
        return Response({
            "data": data,
            "success": success,
            "message": message,
            "score" : score,
            "submission_id" : submission_id
        }, status=status_code)
    else:
        return Response({
            "data": data,
            "success": success,
            "message": message
        }, status=status_code)




class UserMessage:
    USER_SIGNUP_SUCCESSFULLY = 'Your Account Created Succcessfully.'
    USER_LOGIN_SUCCESSFULLY = 'Login Successfully.'
    USER_LOGIN_FAIL = 'Invalid email or password. Please try again.'
    USER_PROFILE_UPDATE_SUCCESSFULLY = 'Your Profile Updated Successfully.'
    USER_CHANGE_PASS_SUCCESSFULLY = 'Your Password Changed Successfully.'
    USER_DETAIL_RETRIEVE_SUCCESSFULLY = 'Your Detail Retrieve Successfully.'
    

class QuizMessage:
    QUIZ_LIST_SUCCESSFULLY = 'All quizzes have been fetched successfully.'
    QUIZ_NOT_FOUND = 'Quiz not found.'
    QUIZ_RETRIEVE_SUCCESSFULLY = 'Quiz fetched successfully.'
    QUIZ_SUBMITTED_SUCCESSFULLY = 'Quiz submitted successfully'


class UserSubmissionMessages:
    USER_SUBMISSION_RETRIEVE_SUCCESSFULLY = 'Your Submission retrieve successfully.'
    USER_RESULT_RETRIEVE_SUCCESSFULLT = 'Quiz result fetched successfully.'


class EventMessages:
    EVENT_FETCHED_SUCCESSFULLY = 'Updacoming Events are fetch successfully'