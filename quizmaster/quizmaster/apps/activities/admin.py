from django.contrib import admin

from .models import Activity, Quiz, Question, QuestionChoice


admin.site.register(Activity)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuestionChoice)
