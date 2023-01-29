from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import SubscribedUsers

@user_not_authenticated
def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request = request,
        template_name = "users/register.html",
        context={"form":form}
        )

def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear &nbsp; <b>{user}</b>, activation link is sent to &nbsp; <b>{to_email}</b>. &nbsp;<b>Note:</b> &nbsp; Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')



@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

@user_not_authenticated
def custom_login(request):
    
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello <b>{user.username}</b>! You have been logged in successfully')
                return redirect('/')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, 'You must pass the reCAPTCHA test')
                    continue
                messages.error(request, error)
    
    form = UserLoginForm()
    
    return render(
        request=request,
        template_name='users/login.html',
        context={"form":form}
    )

def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            
            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)
        
        for error in list(form.errors.values()):
            messages.error(request, error)
    
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', context={'form': form})
    return redirect('/')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('users:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        
    return redirect('/')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully.")
            return redirect('users:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            corresponding_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if corresponding_user:
                subject = 'Password reset request'
                message = render_to_string('users/reset_password_email.html', {
                    'user': corresponding_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(corresponding_user)),
                    'token': account_activation_token.make_token(corresponding_user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[corresponding_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><br/>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, 'Problem sending reset password email, &npsp; <b>SERVER PROBLEM</b>')
            return redirect('/')
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test.")
                continue
        
    form = PasswordResetForm()
    return render(
        request=request,
        template_name='users/password_reset.html',
        context={
            'form': form
        }
    )
    
def password_reset_confirmation(request, uidb64, token):
    User = get_user_model()
    try:
        username = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(username=username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and &nbsp; <b>log in </b> &nbsp; now.")
                return redirect('/')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'users/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")

def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        print(name, email)
        if not name or not email:
            messages.error(request, 'Please use legit name and email to subscribe.')
            return redirect('/')

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f'Found registered user with associated {email} email. You must login to subscribe or unsubscribe.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f'{email} email address is already subscribed.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('/')
        
        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("/")