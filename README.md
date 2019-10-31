Look at example.py
You'll need to replace it with your own config for the resource you'd like to manage.

You'll need to:
1. Configure a Slack App and add the command in the file.
2. You'll need to create a bucket in S3.
3. You'll need to create a resources.json file in the bucket (look at example_rooms.json)
4. You'll need to create an admins.json file in the bucket (look at example_admins.json)
5. You'll need to upload the code to a Lambda function (and configure its path in the Slack bot) and add permissions to S3

to test locally, run:
`python3 example.py`
