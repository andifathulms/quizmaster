import os
import shortuuid

from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from typing import Any


class FilenameGenerator(object):
    """
    Utility class to handle generation of file upload path
    """
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def __call__(self, instance: object, filename: str) -> str:
        today = timezone.localdate()

        filepath = os.path.basename(filename)
        filename, extension = os.path.splitext(filepath)
        filename = slugify(shortuuid.uuid()[:10])

        path = "/".join([
            self.prefix,
            today.strftime('%Y/%m/%d'),
            filename + extension
        ])
        return path


def get_redirect_url(request: HttpRequest, user: Any) -> redirect:
    next = request.GET.get('next')

    if user.is_superuser:
        if user.active_instructor_id:
            redirect_url = next or reverse('instructors:index')
        elif user.active_participant_id:
            redirect_url = next or reverse('participants:index')

    elif user.instructors.exists():
        redirect_url = next or reverse('instructors:index')

    elif user.participants.exists():
        redirect_url = next or reverse('participants:index')

    else:
        logout(request)
        redirect_url = reverse('login')

    if next:
        redirect_url = next

    return reverse('instructors:index')


try:
    from django.utils.deconstruct import deconstructible
    FilenameGenerator = deconstructible(FilenameGenerator)  # type: ignore
except ImportError:
    pass
