import json

class User:
    def __init__(self, userid, username):
        self._userid = userid
        self._username = username

    def get_userid(self):
        return self._userid

    def get_username(self):
        return self._username

    def __eq__(self, other):
        if not isinstance(other, User):
            return False

        return self._username == other.get_username()

    def as_json(self):
        return [self._userid, self._username]

    def from_slack_params(params):
        # First we look for the payload. If it exists, take the data from there. Otherwise, fallback to params.
        if 'payload' in params:
            payload = json.loads(params['payload'][0])
            user_dict = payload.get('user')
            return User(user_dict['id'], user_dict['name'])

        return User(params['user_id'][0], params['user_name'][0])
