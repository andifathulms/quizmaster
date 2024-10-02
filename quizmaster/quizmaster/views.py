from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from quizmaster.core.utils import get_redirect_url


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context_data = {}

    return render(request, "index.html", context_data)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(get_redirect_url(request, request.user))

    auth_form = AuthenticationForm(data=request.POST or None)
    if auth_form.is_valid():
        user = auth_form.get_user()
        login(request, user)
        return redirect(get_redirect_url(request, user))

    context_data = {
        'form': auth_form,
        'title': 'Login'
    }
    return render(request, 'login.html', context_data)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')
