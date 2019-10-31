import json

class AdminRepo:
    def __init__(self, proxy):
        self._proxy = proxy
        self._admins = json.loads(self._proxy.load_from_file())

    def is_admin(self, user):
        return user.get_username() in self._admins
