from django.contrib.auth import get_user_model
from django.db import models

class Survey(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    available_places = models.IntegerField()

    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
