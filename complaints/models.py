from django.db import models


class Complaint(models.Model):
    reported_category = models.CharField(max_length=60)
    predicted_category = models.CharField(max_length=60)
    description = models.TextField()
    location = models.CharField(max_length=160)
    attachment_names = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.predicted_category} - {self.location}"