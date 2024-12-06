import os
from django.shortcuts import render, redirect
from contacts.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def show_contacts_page(request):

    form = ContactForm(request.POST or None)

    form.initial["from_"] = request.user.email
    form.initial["to"] = settings.SENDER_EMAIL

    if request.method == "POST":

        if form.is_valid():

            send_mail(
                "Pesho",
                "Pesho e mn gotin",
                "loopplay12@gmail.com",
                ["mamarida50@gmail.com"],
                fail_silently=False
            )

            return redirect("main-page")


    context = {
        "form": form
    }

    return render(request, "contacts/contact-page.html", context)
