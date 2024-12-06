import asyncio
from asgiref.sync import sync_to_async
from django.core.mail import send_mail


async def send_mail_async(subject, message, from_email, recipient_list):

    await sync_to_async(send_mail)(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False
    )