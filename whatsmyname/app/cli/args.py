import logging
import os.path
import string
import tempfile
from argparse import ArgumentParser
from random import random, choice

from whatsmyname.app.config import project_path
from whatsmyname.app.models.schemas.cli import CliOptionsSchema

logger = logging.getLogger()


def get_default_args() -> ArgumentParser:
    """
    Returns an argument parser with a set of defaults
    :return:
    """
    parser = ArgumentParser(
        description="This standalone script will look up a single username using the JSON file"
                    " or will run a check of the JSON file for bad detection strings.")
    parser.add_argument('-u', '--usernames', nargs='*', help='[OPTIONAL] If this param is passed then this script will perform the '
                                                 'lookups against the given user name instead of running checks against '
                                                 'the JSON file.')
    parser.add_argument('-in', '--input_file', nargs='?',
                        help="[OPTIONAL] Uses a specified file for checking the websites")
    parser.add_argument('-s', '--sites', nargs='*',
                        help='[OPTIONAL] If this parameter is passed the script will check only the named site or list of sites.')
    parser.add_argument('-f', '--found', help="Display found results.", action="store_true", default=False)
    parser.add_argument('-n', '--not_found', help="Display not found results", action="store_true", default=False)
    parser.add_argument('-d', '--debug', help="Enable debug output", action="store_true", default=False)
    parser.add_argument('-o', '--output_file', nargs='?', help="[OPTIONAL] Uses a specified output file ")
    parser.add_argument('-t', '--timeout', nargs='?', help='[OPTIONAL] Timeout per connection, default is 60 seconds.', default=60)
    parser.add_argument('-prt', '--per_request_time', nargs='?', help='[Optional] Timeout per request, default is 5 seconds', default=5)
    parser.add_argument('-fmt', '--format', nargs='?', help='[Optional] Format options are json, csv, or table', default='json')

    return parser


def arg_parser(arguments: ArgumentParser) -> CliOptionsSchema:
    """
    Parse the passed in arguments into something the schema will understand
    :param arguments: ArgumentParser
    :return:
    """
    parsed = vars(arguments)
    schema: CliOptionsSchema = CliOptionsSchema(**parsed)

    # set global logger levels
    if schema.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if not schema.input_file:
        input_file: str = os.path.join(project_path, 'resources', 'wmn-data.json')
        schema.input_file = input_file
        logger.debug('Loading default input file %s', input_file)

    if not os.path.isfile(input_file):
        logger.error('Input file does not exist %s', input_file)
        raise Exception(f'Input file does not exist ${input_file}.')

    if not schema.output_file:
        letters = string.ascii_lowercase
        schema.output_file = os.path.join(tempfile.gettempdir(), ''.join(choice(letters) for _ in range(10)))
        schema.output_stdout = True

    return schema



