"""CLI for MGZ database."""
import argparse
import json
import logging
import os

import coloredlogs
from mgzdb.api import API
from mgzdb.util import parse_series_path


CMD_ADD = 'add'
CMD_REMOVE = 'remove'
CMD_GET = 'get'
SUBCMD_FILE = 'file'
SUBCMD_MATCH = 'match'
SUBCMD_SERIES = 'series'
DEFAULT_DB = 'sqlite:///data.db'


def main(args): # pylint: disable=too-many-branches
    """Handle arguments."""

    db_api = API(
        args.database, args.store_path,
        playback=args.playback,
        voobly_key=args.voobly_key,
        voobly_username=args.voobly_username,
        voobly_password=args.voobly_password
    )

    # Add
    if args.cmd == CMD_ADD:

        db_api.start()

        # File
        if args.subcmd == SUBCMD_FILE:
            for rec in args.rec_path:
                db_api.add_file(rec, args.source, None)

        # Match
        elif args.subcmd == SUBCMD_MATCH:
            for url in args.url:
                db_api.add_match(args.platform, url)

        # Series
        elif args.subcmd == SUBCMD_SERIES:
            for path in args.zip_path:
                series, series_id = parse_series_path(path)
                db_api.add_series(
                    path, series, series_id
                )

    # Remove
    elif args.cmd == CMD_REMOVE:
        db_api.remove(file_id=args.file, match_id=args.match)

    # Get
    elif args.cmd == CMD_GET:
        filename, data = db_api.get(args.file)
        output_filename = args.output_path or filename
        if os.path.exists(output_filename):
            print('file already exists:', output_filename)
            return
        with open(output_filename, 'wb') as handle:
            handle.write(data)
        print(output_filename)


def setup():
    """Setup CLI."""
    coloredlogs.install(
        level='INFO',
        fmt='%(asctime)s [%(process)d]%(name)s %(levelname)s %(message)s'
    )
    logging.getLogger('paramiko').setLevel(logging.WARN)
    logging.getLogger('voobly').setLevel(logging.WARN)
    logging.getLogger('sqlalchemy').setLevel(logging.WARN)

    parser = argparse.ArgumentParser()
    default_file_path = os.path.abspath('.')

    # Global options
    parser.add_argument('-d', '--database', default=os.environ.get('MGZ_DB', DEFAULT_DB))
    parser.add_argument('-sp', '--store-path', default=os.environ.get('MGZ_STORE_PATH', default_file_path))
    parser.add_argument('-ap', '--playback', default=os.environ.get('AOC_PLAYBACK'))
    parser.add_argument('-vk', '--voobly-key', default=os.environ.get('VOOBLY_KEY', None))
    parser.add_argument('-vu', '--voobly-username', default=os.environ.get('VOOBLY_USERNAME', None))
    parser.add_argument('-vp', '--voobly-password', default=os.environ.get('VOOBLY_PASSWORD', None))

    # Commands
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    # "add" command
    add = subparsers.add_parser(CMD_ADD)

    # "add" subcommands
    add_subparsers = add.add_subparsers(dest='subcmd')
    add_subparsers.required = True

    # "add file"
    add_file = add_subparsers.add_parser(SUBCMD_FILE)
    add_file.add_argument('-s', '--source', default='cli')
    add_file.add_argument('--series')
    add_file.add_argument('--tournament')
    add_file.add_argument('rec_path', nargs='+')

    # "add match"
    add_match = add_subparsers.add_parser(SUBCMD_MATCH)
    add_match.add_argument('platform')
    add_match.add_argument('url', nargs='+')

    # "add series"
    add_series = add_subparsers.add_parser(SUBCMD_SERIES)
    add_series.add_argument('zip_path', nargs='+')

    # "remove" command
    remove = subparsers.add_parser(CMD_REMOVE)
    remove_group = remove.add_mutually_exclusive_group(required=True)
    remove_group.add_argument('-f', '--file')
    remove_group.add_argument('-m', '--match')

    # "get" command
    get = subparsers.add_parser(CMD_GET)
    get.add_argument('file')
    get.add_argument('-o', '--output-path')

    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    setup()
