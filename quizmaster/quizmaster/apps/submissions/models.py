from django.db import models

from model_utils import Choices


class Submission(models.Model):
    quiz = models.ForeignKey('activities.Quiz', on_delete=models.CASCADE, related_name='submissions')
    participant = models.ForeignKey('participants.Participant', on_delete=models.CASCADE,
                                    related_name='submissions', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', related_name='submissions', on_delete=models.CASCADE,
                                   blank=True, null=True)
    STATUS = Choices(
        (10, 'submitted', 'Submitted'),
        (20, 'graded', 'Graded')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.submitted)

    grade = models.FloatField(blank=True, null=True, help_text="The total score of the submission.")
    feedback = models.TextField(blank=True, help_text="Optional feedback for the submission.")
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return f"{self.participant} - {self.quiz} ({self.get_status_display()})"


class SubmissionAnswer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('activities.Question', on_delete=models.CASCADE, related_name='answers')
    choice = models.ForeignKey('activities.QuestionChoice', on_delete=models.CASCADE, related_name='answers',
                               blank=True, null=True)
    value = models.TextField(blank=True, null=True)  # For free-text answers

    created = models.DateTimeField(blank=True, null=True)
    is_correct = models.BooleanField(default=False, help_text="Indicates if the answer is correct.")
    points_awarded = models.FloatField(null=True, blank=True, help_text="Points awarded for this answer.")
    feedback = models.TextField(blank=True, help_text="Optional feedback for this answer.")

    def __str__(self):
        return f"{self.question.text[:50]} - {self.value or self.choice}"
