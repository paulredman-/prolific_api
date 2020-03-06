from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.reverse import reverse

from model_bakery import baker

from surveys.models import Survey


class SurveyTestClass(TestCase):
    def test_get_empty_list(self):
        url = reverse('survey-list')

        res = self.client.get(url)
        assert res.status_code == 200

        assert res.json() == []


    def test_get_list_with_survey(self):
        instances = baker.make('Survey', _quantity=5)

        url = reverse('survey-list')

        res = self.client.get(url)
        assert res.status_code == 200

        data = res.json()
        assert len(data) == len(instances)


    def test_get_list_with_user_id(self):
        instances = baker.make('Survey', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey-list'), instances[0].user_id)

        res = self.client.get(url)
        assert res.status_code == 200

        data = res.json()
        assert len(data) == 1


    @override_settings(DEBUG=True)
    def test_get_list_with_invalid_user_id(self):
        baker.make('Survey', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey-list'), 'prr')

        res = self.client.get(url)
        assert res.status_code == 404
        assert res.json() == {"detail":"Not found."}


    def test_get_list_with_non_existent_user_id(self):
        instances = baker.make('Survey', _quantity=2)

        url = '{}?user_id={}'.format(reverse('survey-list'), instances[1].user_id + 1)

        res = self.client.get(url)
        assert res.status_code == 200

        assert res.json() == []


    @staticmethod
    def get_good_input_data():
        user = baker.make(get_user_model())
        return {
            'name': 'Test Survey',
            'user_id': user.id,
            'available_places': 20,
        }


    def test_create(self):
        input_data = self.get_good_input_data()

        url = reverse('survey-list')

        assert Survey.objects.count() == 0
        res = self.client.post(url, data=input_data)
        assert res.status_code == 201
        assert Survey.objects.count() == 1

        output_data = res.json()
        input_data['id'] = output_data['id']
        assert input_data == output_data


    def test_create_missing_data(self):
        good_input_data = self.get_good_input_data()

        url = reverse('survey-list')

        for k in good_input_data:
            input_data = dict(good_input_data)
            del input_data[k]

            assert Survey.objects.count() == 0
            res = self.client.post(url, data=input_data)
            assert res.status_code == 400
            assert Survey.objects.count() == 0


    # I would like to test more bad data values here. However, SQLite is poor at enforcing these.
    # e.g. user_id does not exist, name too long
    # I haven't added validation in the serializer, as this should not be necessary if it works with e.g. PostgreSQL as is.
    # This would work better once a serioius database back-end is used.

    def test_create_bad_data(self):
        good_input_data = self.get_good_input_data()

        bad_input_data = (
            ('user_id', 'prr'),
            ('available_places', 0),
            ('available_places', 'prr'),
        )

        url = reverse('survey-list')

        for k, v in bad_input_data:
            input_data = dict(good_input_data)
            input_data[k] = v

            assert Survey.objects.count() == 0
            res = self.client.post(url, data=input_data)
            assert res.status_code == 400
            assert Survey.objects.count() == 0
