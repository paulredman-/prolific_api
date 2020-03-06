# prolific_api
Coding exercise for Prolific

## Deployment
This has been tested on Windows 10 with Python 3.8 and on Ubuntu 18.04 with Python 3.6

Use the following in a Linux shell to install the development environment, run the tests and start a server
```
mkdir prolific_api
cd prolific_api

python3 -m venv env
git clone git@github.com:paulredman-/prolific_api.git code

source env/bin/activate

cd code

python -m pip install --upgrade pip

# so we can run the tests
pip install -r dev_requirements.txt

cd prolific_api
# check all working OK - 20 tests
py.test

# set up the database
python manage.py migrate

# we need at least one user to create surveys against
python manage.py createsuperuser 

python manage.py runserver &
```

## Example Usage

You may need to `pip install requests`. And then in a Python shell:
```
import requests

# list all surveys - should be none
response = requests.get('http://localhost:8000/surveys')
print(response.json())

# create a survey - assumes user_id=1 for the superuser created above
data = {
    'name': 'Test Survey',
    'available_places': 30,
    'user_id': 1,
}
response = requests.post('http://localhost:8000/surveys', data=data)
print(response.json())

# list all surveys - should be one
response = requests.get('http://localhost:8000/surveys')
print(response.json())

# list all surveys for user - should be one
response = requests.get('http://localhost:8000/surveys?user_id=1')
print(response.json())

# list all surveys for another user - should be none
response = requests.get('http://localhost:8000/surveys?user_id=2')
print(response.json())

# list all surveys responses - should be none
response = requests.get('http://localhost:8000/survey-responses')
print(response.json())

# create a survey response - assumes survey_id=1 for the survey created above
data = {
    'survey_id': 1,
    'user_id': 1,
}
response = requests.post('http://localhost:8000/survey-responses', data=data)
print(response.json())

# list all surveys responses - should be one
response = requests.get('http://localhost:8000/survey-responses')
print(response.json())

# list all surveys responses for user - should be one
response = requests.get('http://localhost:8000/survey-responses?user_id=1')
print(response.json())

# list all surveys responses for another user - should be none
response = requests.get('http://localhost:8000/survey-responses?user_id=2')
print(response.json())

# list all surveys responses for survey - should be one
response = requests.get('http://localhost:8000/survey-responses?survey_id=1')
print(response.json())

# list all surveys responses for another survey - should be none
response = requests.get('http://localhost:8000/survey-responses?survey_id=2')
print(response.json())
```

## Notes
* this uses SQLite3 as its database. This is **not** suitable for production, or even serious development, but is very easy to set up.
* requirements.txt for production, and dev_requirements.txt for development to allow e.g. testing
* the specification talks about both studies and surveys. 

## TODOs
* more docstrings
* move to a production database - either MySQL or PostgreSQL
* test or remove other functionality that is present but possibly not required
  * edit survey and survey-response
  * list all survey responses
* user authorisation
