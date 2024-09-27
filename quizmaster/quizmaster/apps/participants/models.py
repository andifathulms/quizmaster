from django.db import models

from thumbnails.fields import ImageField
from quizmaster.core.utils import FilenameGenerator


class Participant(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='participants')
    photo = ImageField(upload_to=FilenameGenerator(prefix='participants'), blank=True, null=True)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Participant: {self.user.username}"
