from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification(subject, message, recipient_list=None):
    """Отправка простого уведомления мастеру"""
    if recipient_list is None:
        recipient_list = [settings.MASTER_EMAIL]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f"✅ Письмо отправлено: {subject}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False


def send_html_notification(subject, template_name, context, recipient_list=None):
    """Отправка красивого HTML-письма"""
    if recipient_list is None:
        recipient_list = [settings.MASTER_EMAIL]

    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        print(f"✅ HTML-письмо отправлено: {subject}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False