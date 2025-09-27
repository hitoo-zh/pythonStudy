from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)


@shared_task
def sample_task():
    """A simple sample task that simulates some work"""
    logger.info("Starting sample task")
    time.sleep(5)  # Simulate some work
    result = "Sample task completed successfully!"
    logger.info(result)
    return result


@shared_task
def send_email_task(recipient, subject, message):
    """Send email asynchronously"""
    try:
        logger.info(f"Sending email to {recipient}")
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        result = f"Email sent successfully to {recipient}"
        logger.info(result)
        return result
    except Exception as e:
        error_msg = f"Failed to send email to {recipient}: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


@shared_task
def add_numbers(x, y):
    """Simple task to add two numbers"""
    result = x + y
    logger.info(f"Adding {x} + {y} = {result}")
    return result


@shared_task
def process_data_task(data):
    """Process some data asynchronously"""
    logger.info(f"Processing data: {data}")
    # Simulate data processing
    time.sleep(2)
    processed_data = {
        'original': data,
        'processed_at': time.time(),
        'status': 'completed'
    }
    logger.info(f"Data processing completed: {processed_data}")
    return processed_data