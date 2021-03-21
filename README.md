# Conference Management System Backend

This repo organizes the backend of a Conference Management System for Model UN conferences. It aimes to allow smoothless registration and administration of participants, allocation of delegations and general management of a conference.

## Development Instructions

At the moment this project uses Python 3.9.0 and Django 3.1.6

To install the requirements after cloning the code, run

> pip install -r requirements.txt

To start the django project in a server type

> python manage.py runserver

To update the requirements according to your virtual environment, use

> pip freeze > requirements.txt

## Models Diagram

This diagram demonstrates the models and their fields and relationships.

![Models Diagram Image](api_visualization.png)

To generate a diagram from all models excluding the internal classes use

> python manage.py graph_models -a -t original -g --hide-edge-labels -X AbstractBaseSession,Session,User,AbstractBaseUser,PermissionsMixin,AbstractUser,Group,Permission,ContentType,LogEntry -o api_visualization.png

This requires `graphviz` to be installed, e.g. by using `conda install grpahviz`.
