from django.db import models

from thumbnails.fields import ImageField
from quizmaster.core.utils import FilenameGenerator


class Instructor(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='instructors')
    photo = ImageField(upload_to=FilenameGenerator(prefix='instructors'), blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Instructor: {self.user.username}"
