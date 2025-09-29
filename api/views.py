from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from .serializers import UserSerializer, LoginSerializer, TaskSerializer
from tasks.tasks import sample_task, send_email_task
import logging

logger = logging.getLogger(__name__)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def run_sample_task(request):
    """Trigger a sample Celery task"""
    try:
        # Run task asynchronously
        result = sample_task.delay()

        return Response({
            'task_id': result.id,
            'status': 'Task started',
            'message': 'Sample task has been queued'
        })
    except Exception as e:
        logger.error(f"Error starting task: {str(e)}")
        return Response({
            'error': 'Failed to start task'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_email(request):
    """Send email using Celery task"""
    try:
        recipient = request.data.get('email')
        subject = request.data.get('subject', 'Test Email')
        message = request.data.get('message', 'This is a test email sent via Celery.')

        if not recipient:
            return Response({
                'error': 'Email recipient is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Run email task asynchronously
        result = send_email_task.delay(recipient, subject, message)

        return Response({
            'task_id': result.id,
            'status': 'Email queued',
            'message': f'Email to {recipient} has been queued'
        })
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return Response({
            'error': 'Failed to queue email'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_status(request, task_id):
    """Check the status of a Celery task"""
    from celery.result import AsyncResult
    from demo_project.celery import app

    result = AsyncResult(task_id, app=app)

    response_data = {
        'task_id': task_id,
        'status': result.status,
    }

    if result.ready():
        if result.successful():
            response_data['result'] = str(result.result)
        else:
            response_data['error'] = str(result.result)

    return Response(response_data)


def user_logout(request):
    """用户登出视图"""
    logout(request)
    return redirect('/accounts/login/')