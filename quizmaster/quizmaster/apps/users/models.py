from django.contrib.auth.models import AbstractUser
from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=30, db_index=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=254, db_index=True)

    GENDER = Choices(
        (1, "male", 'Male'),
        (2, "female", 'Female')
    )
    gender = models.PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created = AutoCreatedField()

    instructors = models.ManyToManyField('instructors.Instructor', related_name="users",
                                         through='UserToInstructorEdge', through_fields=('user', 'instructor'))
    participants = models.ManyToManyField('participants.Participant', related_name="users",
                                          through='UserToParticipantEdge', through_fields=('user', 'participant'))
    active_instructor_id = models.PositiveIntegerField(blank=True, null=True)
    active_participant_id = models.PositiveIntegerField(blank=True, null=True)


class UserToInstructorEdge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE)


class UserToParticipantEdge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participant = models.ForeignKey('participants.Participant', on_delete=models.CASCADE)
