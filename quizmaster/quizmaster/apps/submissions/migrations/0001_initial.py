# Generated by Django 5.1.1 on 2024-09-27 12:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
        ('participants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(10, 'Submitted'), (20, 'Graded')], default=10)),
                ('grade', models.FloatField(blank=True, help_text='The total score of the submission.', null=True)),
                ('feedback', models.TextField(blank=True, help_text='Optional feedback for the submission.')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='participants.participant')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='activities.quiz')),
            ],
            options={
                'verbose_name_plural': 'Submissions',
            },
        ),
        migrations.CreateModel(
            name='SubmissionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False, help_text='Indicates if the answer is correct.')),
                ('points_awarded', models.FloatField(blank=True, help_text='Points awarded for this answer.', null=True)),
                ('feedback', models.TextField(blank=True, help_text='Optional feedback for this answer.')),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='activities.questionchoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='activities.question')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='submissions.submission')),
            ],
        ),
    ]
