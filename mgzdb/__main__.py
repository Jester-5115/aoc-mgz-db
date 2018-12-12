"""CLI for MGZ database."""
import argparse
import logging
import os

import coloredlogs
import yaml
from mgzdb.api import API


CMD_QUERY = 'query'
CMD_ADD = 'add'
CMD_REMOVE = 'remove'
CMD_TAG = 'tag'
SUBCMD_FILE = 'file'
SUBCMD_MATCH = 'match'
SUBCMD_CSV = 'csv'
SUBCMD_SERIES = 'series'
SUBCMD_SUMMARY = 'summary'
DEFAULT_HOST = 'localhost'
DEFAULT_DB = 'sqlite:///data.db'


def main(args):
    """Handle arguments."""
    db_api = API(
        args.database, args.store_host, args.store_path,
        args.voobly_key, args.voobly_username, args.voobly_password,
        rename=not args.no_rename
    )

    # Add
    if args.cmd == CMD_ADD:

        # File
        if args.subcmd == SUBCMD_FILE:
            for rec in args.rec_path:
                db_api.add_file(
                    rec, args.source, None, args.tags, args.series, args.tournament,
                    force=args.force
                )

        # Match
        elif args.subcmd == SUBCMD_MATCH:
            for url in args.voobly_url:
                db_api.add_url(url, args.download_path, args.tags, force=args.force)

        # Series
        elif args.subcmd == SUBCMD_SERIES:
            db_api.add_series(
                args.zip_path, args.extract_path, args.tags, args.series,
                args.tournament, force=args.force
            )

        # CSV
        elif args.subcmd == SUBCMD_CSV:
            db_api.add_csv(args.csv_path, args.download_path, args.tags, force=args.force)

    # Remove
    elif args.cmd == CMD_REMOVE:
        db_api.remove(file_id=args.file, match_id=args.match, series_id=args.series)

    # Tag
    elif args.cmd == CMD_TAG:
        db_api.tag(args.match, args.tags)

    # Query
    elif args.cmd == CMD_QUERY:
        print(yaml.dump(db_api.query(args.subcmd, **vars(args)), default_flow_style=False))


def setup():
    """Setup CLI."""
    coloredlogs.install(
        level='INFO',
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logging.getLogger('paramiko').setLevel(logging.WARN)
    logging.getLogger('voobly').setLevel(logging.WARN)
    parser = argparse.ArgumentParser()
    default_file_path = os.path.abspath('.')

    # Global options
    parser.add_argument('-d', '--database', default=os.environ.get('MGZ_DB', DEFAULT_DB))
    parser.add_argument('-sh', '--store-host', default=os.environ.get('MGZ_STORE_HOST', DEFAULT_HOST))
    parser.add_argument('-sp', '--store-path', default=os.environ.get('MGZ_STORE_PATH', default_file_path))
    parser.add_argument('-k', '--voobly-key', default=os.environ.get('VOOBLY_KEY', None))
    parser.add_argument('-u', '--voobly-username', default=os.environ.get('VOOBLY_USERNAME', None))
    parser.add_argument('-p', '--voobly-password', default=os.environ.get('VOOBLY_PASSWORD', None))

    # Commands
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True

    # "query" command
    query = subparsers.add_parser(CMD_QUERY)

    # "query" subcommands
    query_subparsers = query.add_subparsers(dest='subcmd')
    query_subparsers.required = True

    # "query match"
    query_match = query_subparsers.add_parser(SUBCMD_MATCH)
    query_match.add_argument('match_id', type=int)

    # "query file"
    query_file = query_subparsers.add_parser(SUBCMD_FILE)
    query_file.add_argument('file_id', type=int)

    # "query series"
    query_series = query_subparsers.add_parser(SUBCMD_SERIES)
    query_series.add_argument('series_id', type=int)

    # "query summary"
    query_subparsers.add_parser(SUBCMD_SUMMARY)

    # "add" command
    add = subparsers.add_parser(CMD_ADD)
    add.add_argument('-f', '--force', action='store_true', default=False)
    add.add_argument('-t', '--tags', nargs='+')
    add.add_argument('-n', '--no-rename', default=False, action='store_true')

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
    add_match.add_argument('voobly_url', nargs='+')
    add_match.add_argument('-dp', '--download-path', default=default_file_path)

    # "add series"
    add_series = add_subparsers.add_parser(SUBCMD_SERIES)
    add_series.add_argument('zip_path')
    add_series.add_argument('series')
    add_series.add_argument('-ep', '--extract-path', default=default_file_path)
    add_series.add_argument('--tournament')

    # "add csv"
    add_csv = add_subparsers.add_parser(SUBCMD_CSV)
    add_csv.add_argument('csv_path')
    add_csv.add_argument('-dp', '--download-path', default=default_file_path)

    # "remove" command
    remove = subparsers.add_parser(CMD_REMOVE)
    remove_group = remove.add_mutually_exclusive_group(required=True)
    remove_group.add_argument('-f', '--file')
    remove_group.add_argument('-m', '--match')
    remove_group.add_argument('-s', '--series')

    # "tag" command
    tag = subparsers.add_parser(CMD_TAG)
    tag.add_argument('match')
    tag.add_argument('tags', nargs='+')

    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    setup()