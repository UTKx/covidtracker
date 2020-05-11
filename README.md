# nCoVTracker
Web application to track the Coronavirus cases implemented with python as back-end and bootstrap as front-end using [NovelCovid API](https://documenter.getpostman.com/view/8854915/SzS7R6uu?version=latest). It displays the current live stats worldwide data and country-wise data.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
+ You need to install [Python3](https://www.python.org/downloads/).
+ After installing you need `virtualenv` to create isolated Python environments. Run the command ```pip install virtualenv``` to install it on your machine.


## Installation and Usage
1. Firstly, get the repo on your machine using [git](https://git-scm.com/) or download it as a zip.
2. Create a virtual environment using command `virtualenv your-environment-name`. Name your environment whatever you like.
3. Now activate your newly created environment.
	+ For Windows users
		- Type `cd file/path/to/your/virtual/environment/scripts` in your terminal.
		- Then type `activate` and your virtual environment  is up and running.
	+ For Linux or Mac users
		- Run `source file/path/to/your/virtual/environment/bin/activate`. This will activate your virtual environment.
4. Go to the project directory using `cd path/to/the/project`
5. Run this command `pip install -r requirements.txt`. This will install all the necessary modules need to run the project.
6. Change your directory to where `manage.py` is located.
7. Run `python manage.py runserver` in your terminal.
8. Go to localhost or type `http://127.0.0.1:8000/` in your browser.

## Built With
+ [Django](https://www.djangoproject.com/) - The web framework used
+ [Bootstrap](https://getbootstrap.com/) - The front-end framework used

# License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/UTKx/covidtracker/blob/master/LICENSE) file for details.