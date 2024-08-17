from django.shortcuts import render
from .forms import MessageForm

# create contact form and send
def contactview(request):
    if request.method == 'POST':
        contact = MessageForm(data=request.POST)

        if contact.is_valid():
            contact.save()
    else:
        contact = MessageForm()

    return render(request, 'contact/contact.html', context={'contact': contact})