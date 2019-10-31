# import inflect
from .bot import *
from .user import *

class SlackHandler(Bot):
    def __init__(self, token, invocation_command, repository, admin_repo=None):
        super().__init__(repository, admin_repo)
        self._token = token
        self._invocation_command = invocation_command

    def _validate_token(self, params):
        token = None
        if 'payload' in params:
            payload = json.loads(params['payload'][0])
            token = payload.get('token')
        else:
            token = params['token'][0]

        if token != self._token:
            raise PermissionError('Invalid request token')

    def help(self, performer, error=None):
        commands = [
            'help - display this help menu',
            'take - ask for a free ' + self._resource_name,
            'release - release a ' + self._resource_name + ' you took',
            'show - show details of a ' + self._resource_name,
            'list - show a list of all ' + self._resource_name, #inflect.engine().plural(self._resource_name),
            'list-mine - show a list of ' + self._resource_name, #inflect.engine().plural(self._resource_name) + ' you took'
        ]
        if not self._admin_repo or self._admin_repo.is_admin(performer):
            commands += [
                'remove - remove a ' + self._resource_name,
                'force-release - release a ' + self._resource_name + ' regardless of who took it'
            ]
        result = { 'attachments': [{ 'title': 'Usage for the bot: ' + self._invocation_command + ' <command name>', 'text': '\n'.join(commands) }] }
        if error:
            result['attachments'] = [{ 'title': 'Error:', 'color': '#F35A00', 'text': error }] + result['attachments']
        return self.respond(result, raw=True)

    def handle(self, params):
        try:
            self._validate_token(params)
        except PermissionError as e:
            print('handle failed with:')
            print(e)
            self.respond(e)

        super().handle(params)

    def respond(self, result, raw=False):
        response = { 'headers': { 'Content-Type': 'application/json' }, 'statusCode': '200' }
        if isinstance(result, Exception):
            response.update({
                'body': json.dumps({ 'attachments': [{ 'title': 'Error:', 'color': '#F35A00', 'text': str(result) }] })
            })
        elif isinstance(result, dict) and not raw:
            response.update({
                'body': json.dumps({ 'response_type': 'in_channel', 'attachments': [{
                        'text': result['title'],
                        'callback_id': result['command'],
                        'color': '#3AA3E3',
                        'actions': [
                            {
                                'name': 'resource_list',
                                'type': 'select',
                                'options': [{ 'text': str(option), 'value': option.get_id() } for option in result['options']]
                            }
                        ]
                    }]
                })
            })
        else:
            response.update({ 'body': json.dumps(result) })
        
        print('Responding with:')
        print(response)
        return response

    def handle(self, params):
        if 'payload' in params:
            payload = json.loads(params['payload'][0])
            
            user_dict = payload.get('user')
            user = User(user_dict['id'], user_dict['name'])

            command = payload.get('callback_id')

            return self.handle_command(user, command, payload.get('actions'))
        else:
            user = User(params['user_id'][0], params['user_name'][0])
            command = params['command'][0]
            if command != self._invocation_command:
                return self.respond(ValueError('Wrong bot, this is "' + self._invocation_command + '"'))

            if 'text' not in params:
                return self.help(user, 'Missing command')

            return self.handle_command(user, params['text'][0])
