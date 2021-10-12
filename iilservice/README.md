
Python Version 
--------------------
python3.7

Installation
------------

1. Install pipenv using ``pip install pipenv``.
2. run ``pipenv shell`` create virtualenv and Pipfile
3. run ``pipenv install`` install packages
4. run ``pipenv run server`` for change enviorment modified this command in pipfile
		[scripts]
		server = "python manage.py runserver --settings=settings.local"

