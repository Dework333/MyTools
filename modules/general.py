import os
import json
from rich import print as rprint
from pathlib import Path


# TEST PATH
path = Path(r'C:\Users\user\Desktop\test\data.json')
if path.exists():
	with open(path, 'r') as f:
		data = json.load(f)
else:
	with open(r'C:\Users\user\Desktop\test\data.json', 'w') as f:
		f.write('{}')


def print_error(error_text: str):
	return (f'[red bold]Error[/]: {error_text}!')


def print_warning():
	return 'warning'


def print_status(status: bool, result: str,  name: str = None, reason: str = None):
	if not status and reason is None:
		return print_error('reason not written')

	if not name:
		name = '[yellow]N/A[/]'

	reason_list = {
		'enough'   : 'Not enough arguments',
		'empty'    : 'List is empty',
		'exist'    : f'{name} already exists',
		'nexist'   : f"{name} doesn't exist",
		'incorrect': 'incorrect task name'
	}

	if not status and reason not in reason_list:
		return print_error('reason not in list')

	is_success = '[bold green] * Successful[/]' if status else '[bold red] * Unsuccesful[/]'
	res_suffix = f'{result}d' if result[-1:] == 'e' else f'{result}ed'
	result_is  = f'{res_suffix}' if status else f'not {res_suffix}' 
	reason_is  = f'Reason: [bold red]{reason_list[reason]}[/]' if not is_success else ""

	return (f'{is_success}: {name} was {result_is}. {reason_is}')


def save(file_path, data):
	pass