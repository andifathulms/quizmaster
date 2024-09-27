from django.db import models
from django.utils import timezone

from model_utils import Choices


class Activity(models.Model):
    name = models.CharField(max_length=255)

    TYPE = Choices(
        (1, 'assignment', 'Assignment'),
        (2, 'quiz', 'Quiz')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, default=TYPE.quiz)

    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=True)

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='activities',
                             null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self) -> str:
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE, related_name='quizzes',
                                   blank=True, null=True)

    DISPLAY_TYPE = Choices(
        (1, 'single_page', 'All questions in one page'),
        (2, 'multiple_pages', 'One question per page')
    )
    display_type = models.PositiveSmallIntegerField(choices=DISPLAY_TYPE, default=DISPLAY_TYPE.single_page)

    STATUS = Choices(
        (1, 'draft', 'Draft'),
        (2, 'published', 'Published'),
        (3, 'archived', 'Archived'),
        (4, 'scheduled', 'Scheduled'),
        (5, 'closed', 'Closed'),
        (6, 'reviewing', 'Reviewing'),
        (7, 'in_progress', 'In Progress')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.draft)

    random_ordering = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(default='', blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True, help_text="test duration in minutes")
    access_code = models.CharField(max_length=20, blank=True, help_text="Optional access code for restricted quizzes")

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self) -> str:
        return self.name

    def is_active(self):
        now = timezone.now()

        if self.is_active:
            if (not self.start_time or self.start_time <= now):
                if (not self.end_time or self.end_time >= now):
                    return True
        return False


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    TYPE = Choices(
        (1, 'multiple_choice', 'Multiple Choice'),
        (2, 'free_text', 'Free Text')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)

    position = models.IntegerField(help_text='Positioned in ascending order, starting from 0')
    is_active = models.BooleanField(default=True)
    score = models.PositiveSmallIntegerField(help_text='Score awarded for a correct answer.',
                                             blank=True, null=True)

    def __str__(self) -> str:
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text


class QuestionChoice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')
    value = models.TextField()
    position = models.IntegerField(help_text='Positioned in ascending order')
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.value

    @property
    def alpha_position(self) -> str:
        return chr(97 + self.position)
