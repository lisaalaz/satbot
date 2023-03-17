# individual_project_backend

You will need to install Python 3 first (3.6 or higher should work fine).

You may want to install virtualenv to store these libraries in one environment:
``` sudo pip install virtualenv ``` then ``` virtualenv [directory] ```

More instructions at: https://python.land/virtual-environments/virtualenv

To activate venv, do `source venv_folder_location/bin/activate `
and to deactivate do `deactivate`

You will need to install libraries using ``` python3 -m pip install -r requirements.txt ```
or ``` pip install -r requirements.txt ```

To set up a database you can use the following commands:
```
set FLASK_APP=flask_backend_with_aws

Commands for the "model" directory:

# ~ Initialize database changes ~ #
flask db init

# ~ Migrate database changes ~ #
flask db migrate -m "testDB table"

# ~ Upgrade database changes ~ #
flask db upgrade

# ~ Launch flask ~ #
flask run <- starts dev server

Commands for root dir:

# To launch gunicorn, cd to individual-project-app (cd ..) then:
gunicorn -b 0.0.0.0:5000 model.flask_backend_with_aws <- prod server

May need to adjust above command to be of following format (used in AWS instance):
gunicorn3 -b 127.0.0.1:5000 -t 600 "model:create_app()"


Can check: https://docs.gunicorn.org/en/stable/run.html
Other useful links:
https://medium.com/@shefaliaj7/hosting-react-flask-mongodb-web-application-on-aws-part-4-hosting-web-application-b8e205c19e4 <- to follow steps to create AWS instance.

https://adamraudonis.medium.com/how-to-deploy-a-website-on-aws-with-docker-flask-react-from-scratch-d0845ebd9da4 <- for some source code to start with if needed (less useful)

https://ryanlstevens.github.io/2019-10-13-Flask-AWS-and-MySQL/ <- for help with mapping Flask to RDS (I only used SQLite for this project)

```
Note when running flask run:
This should be run in a separate terminal tab to the frontend application.

Adjust DB URL to be where your model folder is from the URL below (for .env file):
DATABASE_URL="sqlite:////home/ali/individual-project-app/model/app.db"

Add this to a .env file in the model folder.