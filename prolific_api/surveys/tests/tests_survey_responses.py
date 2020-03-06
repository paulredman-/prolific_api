import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.reverse import reverse

from model_bakery import baker

from surveys.models import SurveyResponse


class SurveyResponseTestClass(TestCase):
    def setUp(self):
        self.survey = None
        self.user = None
        super().setUp()


    def test_get_empty_list(self):
        url = reverse('survey_response-list')

        res = self.client.get(url)
        assert res.status_code == 200

        assert res.json() == []


    def test_get_list_with_survey_response(self):
        instances = baker.make('SurveyResponse', _quantity=5)

        url = reverse('survey_response-list')

        res = self.client.get(url)
        assert res.status_code == 200

        data = res.json()
        assert len(data) == len(instances)


    def test_get_list_with_user_id(self):
        instances = baker.make('SurveyResponse', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey_response-list'), instances[0].user_id)

        res = self.client.get(url)
        assert res.status_code == 200

        data = res.json()
        assert len(data) == 1


    @override_settings(DEBUG=True)
    def test_get_list_with_invalid_user_id(self):
        baker.make('SurveyResponse', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey_response-list'), 'prr')

        res = self.client.get(url)
        assert res.status_code == 404
        assert res.json() == {"detail":"Not found."}


    def test_get_list_with_non_existent_user_id(self):
        instances = baker.make('SurveyResponse', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey_response-list'), instances[1].user_id + 1)

        res = self.client.get(url)
        assert res.status_code == 200

        assert res.json() == []


    def get_good_input_data(self):
        self.survey = baker.make('Survey', available_places=random.randint(20, 40))
        self.user = baker.make(get_user_model())
        return {
            'survey_id': self.survey.id,
            'user_id': self.user.id,
        }


    def test_create(self):
        input_data = self.get_good_input_data()

        url = reverse('survey_response-list')

        assert SurveyResponse.objects.count() == 0
        res = self.client.post(url, data=input_data)
        assert res.status_code == 201
        assert SurveyResponse.objects.count() == 1

        output_data = res.json()
        input_data['id'] = output_data['id']
        input_data['created_at'] = output_data['created_at']
        assert input_data == output_data


    def test_create_missing_data(self):
        good_input_data = self.get_good_input_data()

        url = reverse('survey_response-list')

        for k in good_input_data:
            input_data = dict(good_input_data)
            del input_data[k]

            assert SurveyResponse.objects.count() == 0
            res = self.client.post(url, data=input_data)
            assert res.status_code == 400
            assert SurveyResponse.objects.count() == 0


    # I would like to test more bad data values here. However, SQLite is poor at enforcing these.
    # e.g. user_id does not exist, survey_id does not exist
    # I haven't added validation in the serializer, as this should not be necessary if it works with e.g. PostgreSQL as is.
    # This would work better once a serioius database back-end is used.

    def test_create_bad_data(self):
        good_input_data = self.get_good_input_data()
        bad_input_data = (
            ('user_id', 'prr'),
            ('survey_id', 'prr'),
            ('survey_id', self.survey.id + 1),
        )

        url = reverse('survey_response-list')

        for k, v in bad_input_data:
            input_data = dict(good_input_data)
            input_data[k] = v

            assert SurveyResponse.objects.count() == 0
            res = self.client.post(url, data=input_data)
            assert res.status_code == 400
            assert SurveyResponse.objects.count() == 0


    def test_available_places(self):
        available_places = 5

        self.survey = baker.make('Survey', available_places=available_places)
        self.user = baker.make(get_user_model())
        input_data = {
            'survey_id': self.survey.id,
            'user_id': self.user.id,
        }

        url = reverse('survey_response-list')

        for i in range(available_places):
            assert SurveyResponse.objects.count() == i
            res = self.client.post(url, data=input_data)
            assert res.status_code == 201
            assert SurveyResponse.objects.count() == i + 1

        for i in range(6):
            assert SurveyResponse.objects.count() == available_places
            res = self.client.post(url, data=input_data)
            assert res.status_code == 400
            assert SurveyResponse.objects.count() == available_places
