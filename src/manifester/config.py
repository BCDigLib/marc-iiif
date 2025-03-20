import os

from dotenv import dotenv_values
from getpass import getpass
import argparse

src_dir = os.path.dirname(__file__)
root_dir = os.path.join(src_dir, os.pardir, os.pardir)


class Config:
    """
    All configuration necessary to generate a view/manifest
    """
    image_base: str
    handle_passwd: str
    aspace_passwd: str
    handle_url: str
    ssh: str
    source_record: str
    iiif_base_url: str
    manifest_dir: str
    view_dir: str
    handle_dir: str
    image_dir: str
    verbosity: int
    citation: str
    manifest_filename: str
    view_filename: str


def load_config() -> Config:
    """
    Load the configuration values from command line and env files

    :return: Config all configuration necessary for the run
    """
    args = get_args()
    dotenv = dotenv_values(".env")
    config = Config()

    # These values must come from the CLI arguments.
    config.image_base = args.image_base
    config.source_record = args.source_record
    config.handle_url = args.handle
    config.citation = args.citation
    config.attribution = args.attribution
    config.verbosity = max((30 - args.verbose * 10), 10) if args.verbose > 0 else 0
    config.manifest_filename = args.manifest
    config.view_filename = args.view

    # These must come from the env file.
    config.iiif_base_url = dotenv['IIIF_BASE_URL']

    # These could come from the env file or CLI arguments.
    config.ssh = args.ssh if args.ssh else dotenv['SSH_CREDENTIALS']
    config.image_dir = args.image_dir if args.image_dir else dotenv['IMAGE_DIR']

    # These must either be from the env file or entered by the user at runtime.
    config.handle_passwd = dotenv['HANDLE_PASSWD'] if 'HANDLE_PASSWD' in dotenv else getpass('Handle server password:')
    config.aspace_passwd = dotenv['ASPACE_PASSWD'] if 'ASPACE_PASSWD' in dotenv else getpass('ASpace admin password:')

    # These are either in the env file or use a local default.
    config.manifest_dir = dotenv['MANIFEST_DIR'] if 'MANIFEST_DIR' in dotenv else os.path.join(root_dir, 'manifests')
    config.view_dir = dotenv['VIEW_DIR'] if 'VIEW_DIR' in dotenv else os.path.join(root_dir, 'view')

    # This is hard-coded.
    config.handle_dir = os.path.join(root_dir, 'hdl')

    return config


def get_args():
    """
    Read the command line arguments

    :return: List the submitted arg values
    """
    parser = argparse.ArgumentParser(prog='manifester', add_help=True, description=__doc__)
    parser.add_argument('source_record', help='the source record (MARC file, ASpace record, etc.) to process')
    parser.add_argument('--image_base', help='image file prefix (e.g. ms-2020-020-142452)')
    parser.add_argument('--handle', help='Handle URL')
    parser.add_argument('--ssh', help='IIIF server SSH connection string (ex. florinb@scenery.bc.edu)')
    parser.add_argument('--image_dir', help='image directory on IIIF server')
    parser.add_argument('--citation', help='text of citation')
    parser.add_argument('--attribution', help='text of attribution')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--manifest', help='manifest file name')
    parser.add_argument('--view', help='view file name')
    return parser.parse_args()
