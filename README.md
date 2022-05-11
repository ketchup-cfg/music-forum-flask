
# Heavy Metal Machine: A Music Forum

This is a Python web application built with the Flask framework that provides several REST API endpoints to support the world's least favorite music forum.

The web application is currently built with a RESTful web API service providing backend services, and a frontend built using Jinja2 templates.

## Installing Dependencies

In order to run this application, you will need to install the PyPi packages referenced in the [requirements.txt](https://github.com/ketchup-cfg/learning-flask/blob/main/requirements.txt) file (uh, and also make sure to have Python setup and configured):

```bash
$ pip install -r requirements.txt
```

## Initializing the Database

To ensure that the application actually works, you will also need to initialize the application database:

```bash
$ flask init-db
```

## Running the App

In order to run the application, enter the following command into your terminal (as long as you have installed the app's dependencies and initialized the database):

```bash
$ flask run
```
