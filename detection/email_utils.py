from django.core.mail import EmailMessage
from django.conf import settings

def send_email_alert(image_path, detection_name, current_time, user):
    subject = f"🚨 Alert: {detection_name} Detected!"
    body = f"🔍 {detection_name} was detected at {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n\nImage attached."
    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    if image_path:
        email.attach_file(str(image_path))
    email.send()