# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Here you can do something with the form data, like sending an email
            # Redirect or render a success page
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def verify_contact(request):
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('contact')
    if request.method == 'POST':
        # Process the form data and do necessary actions
        # Once done, clear the session data
        del request.session['form_data']
        return render(request, 'success.html', {'name': form_data['name']})
    return render(request, 'verify_contact.html', {'form_data': form_data})

