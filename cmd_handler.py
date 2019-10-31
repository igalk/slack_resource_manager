import argparse
import os
import traceback
from bot import *
from user import *

class CmdHandler(Bot):
    def __init__(self, repository, admin_repo=None):
        super().__init__(repository, admin_repo)
        self._config_parser()

    def _config_parser(self):
        self._parser = argparse.ArgumentParser(description='CMD mode for the resource manager')
        self._parser.add_argument('command', help='command to run', choices=['help', 'take', 'release', 'show', 'list', 'list-mine', 'remove', 'force-release']) #'add', 'update'])
        self._parser.add_argument('args', nargs=argparse.REMAINDER, help='parameters for the command')

    def help(self, performer, error=None):
        if error:
            print(error)
        self._parser.print_help()

    def respond(self, result):
        if isinstance(result, Exception):
            print('\033[91mError: ' + str(result) + '\n')
            print(''.join(traceback.format_tb(result.__traceback__)))
        elif isinstance(result, list):
            print("\n* ".join(result) + '\n')
        elif isinstance(result, dict):
            print(result['title'])
            print("\n".join(['* ' + str(o) for o in result['options']]) + '\n')
        else:
            print(result + '\n')

    def handle(self):
        args = self._parser.parse_args()
        performer = User(None, os.popen('whoami').read().strip())

        self.handle_command(performer, args.command, *args.args)
