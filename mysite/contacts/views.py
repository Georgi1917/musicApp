from django.shortcuts import render

def show_contacts_page(request):

    return render(request, "contacts/contact-page.html")
