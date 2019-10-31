import os
from urllib.parse import parse_qs

from admin_repo import *
from cmd_handler import *
from slack_handler import *
from files import *
from repository import *

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
BUCKET = 'my-bucket-name'
ROOMS_FILE = 'example_rooms.json'
ADMINS_FILE = 'example_admins.json'

def lambda_handler(event, context):
    bot = SlackHandler(SLACK_WEBHOOK_SECRET, '/rooms', Repository(S3FileProxy(BUCKET, ROOMS_FILE)), AdminRepo(S3FileProxy(BUCKET, ADMINS_FILE)))

    params = parse_qs(event['body'])
    bot.set_resource_name('room')
    print('Got the following params:')
    print(params)
    return bot.handle(params)

def test_local():
    bot = CmdHandler(Repository(LocalFileProxy(ROOMS_FILE)), AdminRepo(LocalFileProxy(ADMINS_FILE)))
    bot.set_resource_name('room')
    bot.handle()
  
if __name__ == "__main__":
  test_local()

