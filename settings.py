# Run ./main.py init to create data.db if you are not using the provided
# training data. You need to delete the old data.db first ONLY IF YOU ARE NOT
# USING THE TRAINING DATA. If you are using the default training data,
# do nothing.
DATABASE_URI = 'sqlite:///data.db'

# This will be auto-created if it does not exist
LOGFILE_URI = 'bot.log'
LOG_LEVEL = 20
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s [%(module)s:%(funcName)s:%(lineno)d]'

SUBREDDIT = 'learnprogramming'
REDIRECT_URI = 'http://127.0.0.1/callback'

# To generate your client id and secret, go to https://www.reddit.com/prefs/apps/
# while logged in as your bot account. Create an app, using any name you like. Set
# the type to 'script', and the 'redirect uri' to http://127.0.0.1/callback
# The string labelled 'secret' is your CLIENT_SECRET, and the other one is your
# CLIENT_ID.
CLIENT_ID = ''
CLIENT_SECRET = ''

# Please use ./main.py create-token to generate this, after setting CLIENT_ID
# and CLIENT_SECRET. It will open your web browser to get permission to
# use OAuth. This only needs to be done once.
CLIENT_ACCESSCODE = 'access_code_here'
