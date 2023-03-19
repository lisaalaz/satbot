**Instructions to run the backend**

You will need to install Python 3 first (3.6 or higher should work fine).

You may want to install virtualenv to store these libraries in one environment. More instructions at: https://python.land/virtual-environments/virtualenv

```
# ~ From outside the repo folder ~ #
virtualenv ./SATbot1.2

# ~ Now cd to the repo folder and activate virtual env ~ #
source bin/activate

# ~ cd to the 'model' folder and execute the following commands ~ #
python3 -m pip install -r requirements.txt
set FLASK_APP=flask_backend_with_aws

# ~ Open rule_based_model.py and change the path of self.data (line 18) to your local path to ep12.csv ~ #

# ~ Initialize database changes ~ #
flask db init

# ~ Migrate database changes ~ #
flask db migrate -m "testDB table"

# ~ Upgrade database changes ~ #
flask db upgrade

# ~ Open .env and add the line DATABASE_URL="sqlite:////[your local path]/app.db". Save and close ~ #

# ~ Optional: set debug mode to true ~ #
export FLASK_DEBUG=1

# ~ Launch flask ~ #
flask run --eager-loading
```
