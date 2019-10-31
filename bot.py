import json
# import inflect

class Bot:
    def __init__(self, repository, admin_repo=None):
        self._repository = repository
        self._admin_repo = admin_repo
        self._resource_name = 'resource'

    def set_resource_name(self, name):
        self._resource_name = name

    def _check_permission(self, performer):
        if self._admin_repo and not self._admin_repo.is_admin(performer):
            raise PermissionError(performer.get_username() + ' is not an admin')

    def assign(self, resource_id, user):
        resource = self._repository.get_resource(resource_id)
        if resource is None:
            return self.respond(ValueError('No ' + self._resource_name + ' with ID=' + resource_id))

        if not resource.is_available():
            return self.respond(ValueError(self._resource_name.capitalize() + ' ' + resource_id + ' is already taken'))

        resource.set_user(user)
        self._repository.commit()
        return self.respond('Assigned ' + self._resource_name + ' ' + resource_id + ' to ' + user.get_username())

    def release(self, performer, resource_id):
        resource = self._repository.get_resource(resource_id)
        if resource is None:
            return self.respond(ValueError('No ' + self._resource_name + ' with ID=' + resource_id))

        if resource.is_available():
            return self.respond(ValueError(self._resource_name.capitalize() + ' ' + resource_id + ' is not taken'))

        if resource.get_user() != performer:
            return self.respond(ValueError(self._resource_name.capitalize() + ' ' + resource_id + ' is taken by someone else'))

        self._repository.get_resource(resource_id).clear_user()
        self._repository.commit()
        return self.respond('Released ' + resource_id)

    def show(self, resource_id):
        resource = self._repository.get_resource(resource_id)
        if resource is None:
            return self.respond(ValueError('No ' + self._resource_name + ' with ID=' + resource_id))

        return self.respond(resource.detailed_str())

    def list(self, user=None):
        resources = []
        if user is None:
            resources = self._repository.all_resources()
        else:
            resources = self._repository.get_resources_for_user(user)

        resources_name = self._resource_name # inflect.engine().plural(self._resource_name)
        if len(resources) == 0:
            if user is None:
                response = 'No ' + resources_name + ' were found'
            else:
                response = 'No ' + resources_name + ' taken'
        else:
            response = [resources_name.capitalize() + ':']
            for resource in resources:
                response.append(str(resource))
            
        return self.respond(response)

    def add_resource(self, performer, resource):
        self._check_permission(performer)
        self._repository.add_resource(resource)
        return self.respond('Added ' + resource)

    def update_resource(self, performer, resource):
        self._check_permission(performer)
        self._repository.update_resource(resource)
        return self.respond('Updated ' + resource)

    def remove_resource(self, performer, resource_id):
        self._check_permission(performer)
        if self._repository.remove_resource(resource_id):
            return self.respond('Removed ' + self._resource_name + ' ' + resource_id)
        else:
            return self.respond(ValueError('No ' + self._resource_name + ' with ID=' + resource_id))

    def force_release(self, performer, resource_id):
        self._check_permission(performer)
        resource = self._repository.get_resource(resource_id)
        if resource is None:
            return self.respond(ValueError('No ' + self._resource_name + ' with ID=' + resource_id))

        if resource.is_available():
            return self.respond(ValueError(self._resource_name.capitalize() + ' ' + resource_id + ' is not taken'))

        resource.clear_user()
        self._repository.commit()
        return self.respond('Released ' + resource_id)

    def handle_command(self, performer, command, *params):
        try:
            if command == 'help':
                return self.help(performer)
            elif command == 'take':
                if len(params) == 0:
                    # present the available resources
                    available = self._repository.available_resources()
                    if len(available) == 0:
                        return self.respond(Exception('All ' + self._resource_name + ' are taken!'))

                    return self.respond({ 'command': 'take', 'title': 'Pick a ' + self._resource_name + ':', 'options': available })

                resource_id = params[0]
                return self.assign(resource_id, performer)
            elif command == 'release':
                if len(params) != 1:
                    return self.respond(ValueError('"release" command takes a ' + self._resource_name + ' ID'))

                resource_id = params[0]
                return self.release(performer, resource_id)
            elif command == 'show':
                if len(params) != 1:
                    return self.respond(ValueError('"show" command takes a ' + self._resource_name + ' ID'))

                resource_id = params[0]
                return self.show(resource_id)
            elif command == 'list':
                return self.list()
            elif command == 'list-mine':
                return self.list(performer)
            # elif command == 'add':
            #     if len(params) != 1:
            #         self.respond(ValueError('"show" command takes a ' + self._resource_name + ' ID'))
            #         return
            #
            #     resource_id = params[0]
            #     resource_details = params[1]
            #     resource = Resource(resource_id, resource_details)
            #     self.add_resource(performer, resource)
            # elif command == 'update':
            #     resource_id = params[0]
            #     resource_details = params[1]
            #     resource = Resource(resource_id, resource_details)
            #     self.update_resource(performer, resource)
            elif command == 'remove':
                if len(params) != 1:
                    return self.respond(ValueError('"remove" command takes a ' + self._resource_name + ' ID'))

                resource_id = params[0]
                return self.remove_resource(performer, resource_id)
            elif command == 'force-release':
                if len(params) != 1:
                    return self.respond(ValueError('"force-release" command takes a ' + self._resource_name + ' ID'))

                resource_id = params[0]
                return self.force_release(performer, resource_id)
            else:
                return self.help(performer, 'Unknown command "' + command + '"')

        except Exception as e:
            return self.respond(e)
