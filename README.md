# Description

Django API to get min, max, average and median temperature and humidity for given city and period of time.
Fetches weather info from api.forecast.io


# Installation

* Install and activate virtualenv. mkvirtualenv recommended. More info here: https://virtualenvwrapper.readthedocs.io/en/latest/

	mkvirtualenv env1

* Install requirements: 
	
	pip install -r requirements.txt


* Run web app locally:

	python manage.py migrate
	python manage.py runserver 

* Example:

	From web browser: http://127.0.0.1:8000/weatherapi/?city=London&from_date=2016-05-01 4:00&to_date=2016-05-02 18:00
	From command line: curl -v -L "http://127.0.0.1:8000/weatherapi/?city=London&from_date=2016-05-01%204:00&to_date=2016-05-02%2018:00"
