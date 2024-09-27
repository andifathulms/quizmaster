from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text='Describe the organization')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
