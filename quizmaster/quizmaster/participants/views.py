from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context_data = {}

    return render(request, "index.html", context_data)