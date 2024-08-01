### Set Up

This was all tested on both Python 3.10 and Python 3.11 (other versions may have issues)
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

### Trouble Shooting

If the database gets into a bad state, you can reset it. You'll need to delete these files:
- predictions/migrations/0001_initial.py
- predictions/migrations/0002_rename_predicted_price_stockprediction_current_price_and_more.py
- db.sqlite3

Then run `python manage.py makemigrations` to regenerate the database migration files.
Then run `python manage.py migrate` to reapply the migrations to the new database.
Then it should work correctly again.