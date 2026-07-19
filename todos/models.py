from django.conf import settings
from django.db import models
from django.utils import timezone


class Todo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos",
    )
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return (
            self.due_date is not None
            and self.due_date < timezone.localdate()
            and not self.completed
        )

    def __str__(self):
        return self.title