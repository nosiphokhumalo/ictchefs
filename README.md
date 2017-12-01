# CHEFREG

This is a web-based data management system created for [Infinity Culinary Training](www.ictchefs.org/) as part of the CHEFREG project.In this project, we created software prototypes of a data management tool, which was divided up into three parts:
- [Mobile application](https://github.com/sewagodimo/ChefSchoolAndroidApp)
- Web-based data management tool with the following components:
    - Data entry
    - Data reporting
    - Data management

## COLLABORATORS
- [Nosipho Khumalo](https://github.com/nosiphokhumalo/)
- [Amy Brodie](https://github.com/AmyLBrodie)
- [Ednecia Matlapeng](https://github.com/sewagodimo)


## FEATURES
 1. Store student information
 2. View overall statistics
 3. Filter statistics by year(s) of admission or class number(s)
 4. View all student information
 5. View/edit/delete a specific student's information
 6. Sort, filter and search student information

## REQUIREMENTS

- Python 3.6.3
- Django 1.11.7

## RUNNING THE PROJECT
1. Clone this repo
2. Ensure that Django is installed
3. Navigate into the root directory of the project
4. Install the required libraries
  - ```pip3 install -r requirements.txt```
5. Make the necessary migrations
  - ```python3 manage.py makemigrations```
  - ```python3 manage.py migrate```
6. Run the project
  - ```python3 manage.py runserver```
# SCREENSHOTS

### Home Page
![](static/img/menu.png "Home Page")

### Add New Student
![](static/img/add.png "Add New Student")

### View Students
![](static/img/view.png "View Students")

### View Statistics
![](static/img/statistics.png "View Statistics")
