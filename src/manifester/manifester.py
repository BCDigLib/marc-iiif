"""
Produce a IIIF-compliant JSON manifest from a binary MARC file and a folder full of JP2s
"""

import json
from datetime import datetime

from pymarc import MARCReader, Field
import requests
import sys
import argparse
import getpass
import glob

from manifester.alma_record import AlmaRecord
from manifester.image import Image
from manifester.source_record import SourceRecord
from ssh_connection import SSHConnection

base_url = 'https://iiif.bc.edu/iiif/2/'


def main():
    """
    Main process
    """
    # Die early if the Python version isn't up to snuff
    check_requirements()

    # Get command line args. We'll prompt the user for a Handle password if they haven't entered one.
    parser = argparse.ArgumentParser(prog='manifester', add_help=True, description=__doc__)
    parser.add_argument('--image_base', help='image file prefix (e.g. ms-2020-020-142452)')
    parser.add_argument('--handle_passwd', help='Handle server password')
    parser.add_argument('--image_dir', help='local directory containing JP2 files')
    parser.add_argument('--ssh', help='IIIF server SSH connection string (ex. florinb@scenery.bc.edu)')
    parser.add_argument('marc_file', help='name of the marc file')
    args = parser.parse_args()

    # Build a connection for SFTPing files if they entered an SSH connection string.
    if args.ssh:
        remote_dir = SSHConnection(args.ssh, '/opt/cantaloupe/images')
    else:
        remote_dir = None

    # List the local image files, if requested. If they just provided SSH credentials, look
    # for the images on that server.
    if args.image_dir:
        glob_pattern = f'{args.image_dir}/{args.image_base}*jp2'
        image_filenames = glob.glob(glob_pattern)
    elif remote_dir:
        image_filenames = remote_dir.list_images(args.image_base)
    else:
        # @todo get a list of files directly from Cantaloupe
        image_filenames = []
    image_filenames.sort()

    images = [Image(filename) for filename in image_filenames]

    hdl_passwd = args.handle_passwd if args.handle_passwd else getpass.getpass('Handle server password:')
    hdl_create_statements = []

    source_record = None

    with open(args.marc_file, 'rb') as bibs:
        reader = MARCReader(bibs)
        # initial for-loop lets you process a collection with multiple records if necessary
        for source_record in reader:
            source_record = AlmaRecord(source_record)

            # Use an identifier from the record unless the user has specified something else.
            identifier = args.image_base if args.image_base else source_record.identifier

            manifest = build_manifest(image_files, source_record)

            write_manifest_file(identifier, manifest)

            view = build_view(identifier, source_record)
            write_view_file(identifier, view)

            hdl_create_statements.append(build_handles(identifier, hdl_passwd, mms))

    bibs.close()

    write_hdl_batchfile(hdl_create_statements)


def write_view_file(identifier: str, view: str) -> None:
    """
    Write a single view file

    :param identifier: str the identifier
    :param view: str the view file contents
    :return: None
    """
    view_file = open('view/' + identifier, 'w')
    view_file.write(view)
    view_file.close()


def write_manifest_file(identifier, manifest):
    manifest_file = open('manifests/' + identifier + '.json', 'w')
    manifest_file.write(json.dumps(manifest))
    manifest_file.close()


def write_hdl_batchfile(hdl_create_statements):
    hdl_file_title = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    hdl_out = open('hdl/handles-' + hdl_file_title + '.txt', 'w')
    all_hdl_create_statements = '\n'.join(hdl_create_statements)
    hdl_out.write(all_hdl_create_statements)
    hdl_out.close()


def build_view(identifier: str, record: object):
    """
    Build view file text

    :param identifier: str the identifier
    :param record: object the MARC record
    :return:str the text of the view file
    """
    # Build from an HTML template.
    with open('view-template.html') as fh:
        html = fh.read()
    html = html.replace('__RECORD_TITLE__', record.title)
    html = html.replace('__RECORD_IDENTIFIER__', identifier)
    return html


def build_handles(identifier, hdl_password, mms: str):
    """
    Build Handle bulk file

    :param identifier: str the identifier
    :param hdl_password: str the Handle server password
    :param mms: str the MMS number of the MARC record
    :return: str the text of the Hanlde bulk file
    """
    # Build from a text template.
    with open('handle-template.txt') as fh:
        hdl_text = fh.read()
    hdl_text = hdl_text.replace('__RECORD_IDENTIFIER__', identifier)
    hdl_text = hdl_text.replace('__RECORD_MMS__', mms)
    hdl_text = hdl_text.replace('__HANDLE_PASSWORD__', hdl_password)
    return hdl_text


def check_requirements():
    """
    Throw an error if something is amiss

    :return: None
    """
    # Uses Literal String Interpolation, available only in Python 3.6+
    if sys.version_info < (3, 6):
        raise Exception('Requires python 3.6 or higher')
