import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .forms import LoginForm, RegisterForm


logger = logging.getLogger(__name__)


def _add_form_errors_to_messages(request, form):
    for errors in form.errors.values():
        for error in errors:
            messages.error(request, error)


def _build_unique_username(email: str) -> str:
    username = email
    index = 1
    while User.objects.filter(username=username).exists():
        index += 1
        username = f"{email.split('@')[0]}{index}"
    return username


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def login_account_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            _add_form_errors_to_messages(request, form)
            return render(request, 'account/login.html', {'form': form}, status=400)

        email = form.cleaned_data['email'].strip().lower()
        password = form.cleaned_data['password']

        try:
            username = (
                User.objects.filter(email=email)
                .values_list('username', flat=True)
                .first()
                or email
            )
            user = authenticate(request, username=username, password=password)
        except Exception:
            logger.exception('Unexpected error during login for email=%s', email)
            messages.error(request, 'Could not sign in right now. Please try again.')
            return redirect('login')

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

        login(request, user)
        messages.success(request, 'Welcome back!')
        logger.info('User login successful for user_id=%s', user.id)
        return redirect('home')

    return render(request, 'account/login.html', {'form': LoginForm()})


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            _add_form_errors_to_messages(request, form)
            return render(request, 'account/register.html', {'form': form}, status=400)

        email = form.cleaned_data['email'].strip().lower()
        password = form.cleaned_data['password']

        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
        except Exception:
            logger.exception('Unexpected error during registration lookup for email=%s', email)
            messages.error(request, 'Could not create account right now. Please try again.')
            return redirect('register')

        username = _build_unique_username(email)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
        except IntegrityError:
            messages.error(request, 'Could not create account. Try again.')
            return redirect('register')
        except Exception:
            logger.exception('Unexpected error creating account for email=%s', email)
            messages.error(request, 'Could not create account right now. Please try again.')
            return redirect('register')

        login(request, user)
        messages.success(request, 'Account created successfully.')
        logger.info('User registration successful for user_id=%s', user.id)
        return redirect('home')

    return render(request, 'account/register.html', {'form': RegisterForm()})
    
@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out.')
    return redirect('login')

