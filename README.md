# CHEFREG

This is a web-based data management system created for [Infinity Culinary Training](www.ictchefs.org/) as part of the CHEFREG project.In this project, we created software prototypes of a data management tool, which was divided up into three parts:
- [Mobile application](https://github.com/sewagodimo/ChefSchoolAndroidApp)
- Web-based data management tool with the following components:
    - Data entry
    - Data reporting
    - Data management

## Collaborators
- [Nosipho Khumalo](https://github.com/nosiphokhumalo/)
- [Amy Brodie](https://github.com/AmyLBrodie)
- [Ednecia Matlapeng](https://github.com/sewagodimo)


## Features
 1. Store student information
 2. View overall statistics
 3. Filter statistics by year(s) of admission or class number(s)
 4. View all student information
 5. View/edit/delete a specific student's information
 6. Sort, filter and search student information

## Requirements

- Python 3.6.3

## Running the project
- Ensure that Django is installed
- Clone this repository
  - ```git clone https://github.com/nosiphokhumalo/ictchefs.git && cd ictchefs```
- Install the required libraries
  - ```pip3 install -r requirements.txt```
- Make the necessary migrations
  - ```python3 manage.py makemigrations```
  - ```python3 manage.py migrate```
- Run the project
  - ```python3 manage.py runserver```

## Deploying on Heroku
- Install the [Heroku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli)
  - Sign up to Heroku
  - Open a terminal and login to your account:
    - ```heroku login```
- Clone this repository:
  - ```git clone https://github.com/nosiphokhumalo/ictchefs.git && cd ictchefs```
- Login to Heroku using the Toolbelt:
  - ```heroku login```
- Inside the project root, create a Heroku app:
  - ```heroku create test-ictchefs``` or ```heroku create``` if you want Heroku to pick a name for you
- Add a MySQL database to your app:
  - ```heroku addons:create cleardb:ignite```
- Push to deploy:
  - ```git push heroku master```
- Migrate the database:
  - ```heroku run python manage.py migrate```
