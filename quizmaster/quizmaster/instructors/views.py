from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest) -> HttpResponse:
    instructor = request.user.get_instructor()

    context_data = {
        "title": "Dashboard",
        "instructor": instructor
    }
    return render(request, "instructors/index.html", context_data)