from os import environ

# the token you get from botfather
BOT_TOKEN = environ['BOT_TOKEN']

# the chat_id of the maintainer, used to alert about possible errors.
# leave empty to disable this feature.
# note that leaving empty also disables the /sendto command
MAINTAINER_ID = environ['MAINTAINER_ID']

APP_NAME = environ['APP_NAME']

PORT = int(environ.get('PORT', 5000))

WEBHOOK_URL = 'https://' + APP_NAME + '.herokuapp.com/' + BOT_TOKEN
