from django.http import Http404

from rest_framework import viewsets

from surveys.models import Survey, SurveyResponse
from surveys.serializers import SurveyResponseSerializer, SurveySerializer

class SurveyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and Survey instances.
    """
    serializer_class = SurveySerializer

    def get_queryset(self):
        """
        Allow filtering on user_id parameter
        """
        queryset = Survey.objects

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            try:
                queryset = queryset.filter(user_id=user_id)
            except ValueError:
                raise Http404('Not a valid integer')

        return queryset.all()


class SurveyResponseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and SurveyResponse instances.
    """
    serializer_class = SurveyResponseSerializer

    def get_queryset(self):
        queryset = SurveyResponse.objects

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            try:
                queryset = queryset.filter(user_id=user_id)
            except ValueError:
                raise Http404('Not a valid integer')

        return queryset.all()
