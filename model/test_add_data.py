import sqlite3
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# ~ Local URI ~ #
local_uri = os.environ.get('DATABASE_URL')
            # or \
            # 'sqlite:///' + os.path.join(basedir, 'app.db')
print(local_uri)
# ~ Connect to database ~ #
conn = sqlite3.connect(local_uri)
c = conn.cursor()


# ~~~ Add data ~~~ #
def insert_row_to_tbl(cursor, table_name, column_names, data_to_add,
                      data_types):
    # Form query
    query = ''' INSERT INTO ''' + table_name + '(' + ','.join(
        column_names) + ') ' + \
            'VALUES(' + ','.join(data_types) + ')'
    # Execute query
    cursor.execute(query, data_to_add)


# ~ Data to add ~ #
colNames = ['username', 'age', 'gender']
data_to_enter = [('test1', 1, 'male'),
                 ('test2', 2, 'female')]

# ~ Add data ~ #
for row in data_to_enter:
    insert_row_to_tbl(c, 'user', colNames, row, ['?', '?', '?'])

# ~~~ Select data from sql table ~~~ #
c.execute('SELECT * FROM user')
