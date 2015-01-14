from app import app

DATABASE = 'tmp/db.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# moved to bottom - maybe use later if at all
# # taken from http://flask.pocoo.org/snippets/104/ - read a secret key from a file
# import sys
# import os.path

# def install_secret_key(app, filename='secret_key'):
#     """Configure the SECRET_KEY from a file
#     in the instance directory.

#     If the file does not exist, print instructions
#     to create it from a shell with a random key,
#     then exit.

#     """
#     filename = os.path.join(app.instance_path, filename)
#     try:
#         app.config['SECRET_KEY'] = open(filename, 'rb').read()
#     except IOError:
#         print 'Error: No secret key. Create it with:'
#         if not os.path.isdir(os.path.dirname(filename)):
#             print 'mkdir -p', os.path.dirname(filename)
#         print 'head -c 24 /dev/urandom >', filename
#         sys.exit(1)

# # cross-site request forgery prevention
# WTF_CSRF_ENABLED = True
# # secret key
# SECRET_KEY = '\\xf1j\\x8c\\x85+V\\xe7;\\xef\\x1d\\x0f\\x89\\xce`\\x06#\\x8a}\\xbd"\\xde\\x10\\xbfJ' #install_secret_key(app)

# OPENID_PROVIDERS = [
#     {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'}
#     ]