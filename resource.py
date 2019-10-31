from user import *

class Resource:
    def __init__(self, id, details, user=None):
        """
        id : unique ID for the resource.
        details : a dictionary of data to store for this resource.
        user : if provided, the user who holds the resource. If not provided, the resource is currently vacant.
        """
        self._id = id
        self._details = details
        self._user = user

    def get_id(self):
        return self._id

    def is_available(self):
        return self._user is None

    def get_user(self):
        return self._user

    def set_user(self, user):
        self._user = user

    def clear_user(self):
        self._user = None

    def get_details(self):
        return self._details

    def set_details(self, details):
        self._details = details

    def as_json(self):
        user = None if self._user is None else self._user.as_json()
        return { 'id': self._id, 'details': self._details, 'user': user }

    def from_json(resource_json):
        user = User(*resource_json['user']) if resource_json['user'] else None
        return Resource(resource_json['id'], resource_json['details'], user)

    def __str__(self):
        display = self._id
        if not self.is_available():
            display += ' (assigned to ' + str(self.get_user().get_username()) + ')'
        return display

    def detailed_str(self):
        display = 'ID: ' + self._id + '\n'
        display += 'Details: ' + '\n'
        for k, v in self._details.items():
            display += '  ' + k + ': ' + str(v) + '\n'
        if self.is_available():
            display += 'User: Unassigned'
        else:
            display += 'User: ' + str(self.get_user().as_json())
        return display
