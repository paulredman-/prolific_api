from django.core.validators import MinValueValidator

from rest_framework import serializers

from surveys.models import Survey, SurveyResponse


class SurveySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    available_places = serializers.IntegerField(validators=[MinValueValidator(1)])
    user_id = serializers.IntegerField()


    def create(self, validated_data):
        """
        Create and return a new `Survey` instance, given the validated data.
        """
        return Survey.objects.create(**validated_data)


    def update(self, instance, validated_data):
        raise NotImplementedError


class SurveyResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    survey_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        """
        Create and return a new `Survey Response` instance, given the validated data.

        We need to validate that we don't have too many responses for the survey.
        For production-ready code, this is complex, as you might have 2 responses submitted at the "same time".
        I would suggest the following algorithm (to be safe) - not implemented here

        # pseudo-code
        If number of responses < available places:
            create this one
        If number of responses > available places:
            # others have also been created
            if our response is in the first available places (sorted by id):
                return it
            else:
                delete it and return an error
        """
        try:
            survey = Survey.objects.get(id=validated_data['survey_id'])
        except Survey.DoesNotExist:
             raise serializers.ValidationError("Survey does not exist")
        survey_response_count = SurveyResponse.objects.filter(survey_id=survey.id).count()
        if survey_response_count >= survey.available_places:
             raise serializers.ValidationError("No places remaining")

        return SurveyResponse.objects.create(**validated_data)


    def update(self, instance, validated_data):
        raise NotImplementedError
