from django.contrib.auth.models import AbstractUser
from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField

from quizmaster.apps.instructors.models import Instructor
from quizmaster.apps.participants.models import Participant

from typing import Optional


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

    def get_instructor(self) -> Optional[Instructor]:
        if hasattr(self, '_instructor'):
            return self._instructor

        if self.is_superuser and self.active_instructor_id:
            instructor = Instructor.objects.filter(id=self.active_instructor_id).first()
            if instructor:
                self._instructor: Optional[Instructor] = instructor
            else:
                self.active_instructor_id = None
                self.save(update_fields=['active_instructor_id'])

                self._instructor = None

        else:
            self._instructor = self.instructors.first()

        return self._instructor

    def get_participant(self) -> Optional[Participant]:
        if hasattr(self, '_participant'):
            return self._participant

        if self.is_superuser and self.active_participant_id:
            participant = Participant.objects.filter(id=self.active_participant_id).first()
            if participant:
                self._participant: Optional[Participant] = participant
            else:
                self.active_participant_id = None
                self.save(update_fields=['active_participant_id'])

                self._participant = None

        else:
            self._participant = self.participants.first()

        return self._participant


class UserToInstructorEdge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE)


class UserToParticipantEdge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    participant = models.ForeignKey('participants.Participant', on_delete=models.CASCADE)
