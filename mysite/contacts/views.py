import os
from django.shortcuts import render, redirect
from contacts.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def show_contacts_page(request):

    form = ContactForm(request.POST or None)

    form.initial["from_"] = request.user.email

    if request.method == "POST":

        if form.is_valid():

            send_mail(
                "Your Contact Form Has Been Received",
                "We would like to inform you that your contact form has reached  us. \nA response will be delivered soon!\n\n  -  The Loop Play Team.",
                settings.SENDER_EMAIL,
                [request.user.email],
                fail_silently=False
            )

            send_mail(
                form.cleaned_data["subject"],
                f"{form.cleaned_data["content"]} \n\nFrom: {request.user.email}",
                request.user.email,
                [settings.SENDER_EMAIL],
                fail_silently=False
            )

            return redirect("main-page")


    context = {
        "form": form
    }

    return render(request, "contacts/contact-page.html", context)
