import json
from .resource import *

class Repository:
    def __init__(self, proxy):
        self._proxy = proxy
        self._load_resources()

    def _load_resources(self):
        resources = json.loads(self._proxy.load_from_file())
        self._resources = { id:Resource.from_json(resources[id]) for id in resources }

    def _save_resources(self):
        resources = json.dumps({ resource:self._resources[resource].as_json() for resource in self._resources })
        self._proxy.store_to_file(resources)

    def commit(self):
        self._save_resources()

    def all_resources(self):
        return [self._resources[id] for id in self._resources]

    def available_resources(self):
        return [self._resources[id] for id in self._resources if self._resources[id].is_available()]

    def get_resource(self, id):
        return self._resources[id] if id in self._resources else None

    def add_resource(self, resource):
        self._resources[resource.get_id()] = resource
        self._save_resources()

    def update_resource(self, resource):
        self.add_resource(resource)

    def remove_resource(self, id):
        if id not in self._resources:
            return False

        del self._resources[id]
        self._save_resources()
        return True

    def take_resource(self, id, user):
        if not self._resources[id].is_available():
            return False

        self._resources[id].set_user(user)
        self._save_resources()
        return True

    def release_resource(self, id):
        self._resources[id].clear_user()
        self._save_resources()

    def get_resources_for_user(self, user):
        return [resource for resource in self._resources.values() if resource.get_user() == user]
