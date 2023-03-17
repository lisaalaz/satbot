# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# # File Name: config.py
# #
# # Sets sqlalchemy uri variable to value specified in .env
# #  file
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# import os
# from dotenv import load_dotenv

# # Absolute directory path
# basedir = os.path.abspath(os.path.dirname(__file__))
# # # print("BASEDIR:", basedir)

# # Looks for and loads .env file
# # Can access env variables using os.environ.get(<VARNAME>)
# load_dotenv(os.path.join(basedir, '.env'))

# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# SQLALCHEMY_TRACK_MODIFICATIONS = False


# # ~ Create config object ~ #
# class Config(object):
#     # ~~ Migration Repository ~~ #
#     SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'model')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
