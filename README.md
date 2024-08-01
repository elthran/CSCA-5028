### Set Up

Everything should already be set up.
The API calls are located at predictions/views.py
Note, if my API key usage is exceeded for the day then it pulls from a static csv

First create a virtual env

`python -m venv venv`

Then enter it

`source venv/bin/activate`

Then install all requirements to it

`pip install -r requirements.txt`

Now in the same terminal run `python manage.py runserver` and leave it running

This should run the Django web app. Now you can go to http://127.0.0.1:8000/
in your browser to interact with the web app. To call the API hit the "Refresh Prediction" button.