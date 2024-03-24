from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.contrib.auth.models import User

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to session for confirmation
            request.session['form_data'] = form.cleaned_data
            
            # Generate email verification token
            user = request.user
            email_verification_token = default_token_generator.make_token(user)
            
            # Build verification URL
            current_site = get_current_site(request)
            verification_url = reverse('verify_contact')
            verification_url = f'http://{current_site.domain}{verification_url}?token={email_verification_token}'
            
            # Send verification email
            subject = 'Email Verification'
            message = render_to_string('email_verification.html', {
                'user': user,
                'verification_url': verification_url,
            })
            send_mail(subject, message, None, [user.email])
            
            # Redirect to the verification page
            return redirect('verify_contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def verify_contact(request):
    token = request.GET.get('token')
    if token is None:
        return redirect('contact')  # Redirect to contact page if no token provided
    
    # Verify token and mark email as verified
    try:
        user_id = default_token_generator.check_token(token)
        user = User.objects.get(pk=user_id)
        user.email_verified = True
        user.save()
        # Optionally, you can redirect to a success page
        return render(request, 'verification_success.html')
    except:
        # Token is invalid or expired, redirect to error page or contact page
        return render(request, 'verification_error.html')
